import streamlit as st
import time
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests

# Replace with your endpoint and prediction key
ENDPOINT = "https://kidneydataset-prediction.cognitiveservices.azure.com/"
PREDICTION_KEY = "58a68df1714b4a49a52bfb52deaed60d"
API_TOKEN = 'HJaeFtURjyS_Li39VxQJokDxSS4QUpVz4thesMoF'
account_id ="7b9a0aec2d148d684d28a3c7645ce0a7"

# Create a prediction client
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

st.set_page_config(page_title="HealthOracle: Decode Your Health")


doctors = [
    {
        "name": "Dr. Harshavardhan Bajoria",
        "specialization": "Nephrologist",
        "location": "Ahemdabad",
        "available_days": "Wed, Thu, Sun",
        "contact": "hvbajoria@hotmail.com",
    },
    {
        "name": "Dr. Soumya Upadhyay",
        "specialization": "Nephrologist",
        "location": "Hyderabad",
        "available_days": "Mon, Tue, Sat",
        "contact": "usoumya19@gmail.com",
    },
    # Add more doctors here...
]

def book_appointment(doctor_name, patient_email, patient_name):
    # Add your booking logic here, e.g., database integration, etc.


    # Send confirmation email to the patient
    send_confirmation_email(patient_email, doctor_name, patient_name)


    # Send appointment email to the doctor
    doctor_email = get_doctor_email(doctor_name)
    send_appointment_email(doctor_email, patient_email, doctor_name, patient_name)


    st.success(f"Appointment booked with {doctor_name}. You will be contacted soon!")


def send_confirmation_email(patient_email, doctor_name,patient_name):
   # Replace 'your_azure_logic_app_url' with the URL of your Azure logic app to send appointment emails
    azure_logic_app_url = "https://prod-11.centralindia.logic.azure.com/workflows/a845897faa254f93a5db7375a917acc7/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qJUCl1H4fqe0QGHrhZQonWcYbCIM_W2Pv7sZElzdTLg"

    email_data = {
        "to": patient_email,
         "name": patient_name,
        "subject": "Appointment Confirmed at HealthOracle",
        "content": f"Your appointment with {doctor_name} has been booked successfully. You will be contacted soon.",
    }


    response = requests.post(azure_logic_app_url, json=email_data)
    if response.status_code == 200 or response.status_code == 202:
        st.success("Confirmation email sent to the patient.")
    else:
        st.error("Failed to send confirmation email.")


def send_appointment_email(doctor_email, patient_email, doctor_name, patient_name):
    # Replace 'your_azure_logic_app_url' with the URL of your Azure logic app to send appointment emails
    azure_logic_app_url ="https://prod-11.centralindia.logic.azure.com/workflows/a845897faa254f93a5db7375a917acc7/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qJUCl1H4fqe0QGHrhZQonWcYbCIM_W2Pv7sZElzdTLg"

    email_data = {
        "to": doctor_email,
        "name": doctor_name,
        "subject": "New Appointment at HealthOracle",
        "content": f"A new appointment has been booked with you by {patient_name}. \n More details will be shared soon.",
    }


    response = requests.post(azure_logic_app_url, json=email_data)
    if response.status_code == 200 or response.status_code == 202:
        st.success("Appointment email sent to the doctor.")
    else:
        st.error("Failed to send appointment email.")


def get_doctor_email(doctor_name):
    # Replace this function with a method to retrieve the doctor's email from your database or list
    # In this example, we'll assume the email is stored in the 'contact' field of the doctor's details.
    for doctor in doctors:
        if doctor["name"] == doctor_name:
            return doctor["contact"]


def doctor():
    st.write("Select a doctor to view details and book an appointment:")
    selected_doctor = st.selectbox("Select a doctor", [doctor["name"] for doctor in doctors])


    # Add an input field for the patient's email
    patient_email = st.text_input("Enter your email", "")
    patient_name = st.text_input("Enter your name", "")


    if st.button("Book Appointment"):
        if not patient_email:
            st.warning("Please enter your email.")
        if not patient_name:
            st.warning("Please enter your name.")
        else:
            book_appointment(selected_doctor, patient_email, patient_name)


    for doctor in doctors:
        if doctor["name"] == selected_doctor:
            st.subheader(doctor["name"])
            st.write(f"Specialization: {doctor['specialization']}")
            st.write(f"Location: {doctor['location']}")
            st.write(f"Available Days: {doctor['available_days']}")

def bot_response(question):
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
    headers = {"Authorization": f"Bearer {API_TOKEN}",'Content-Type': 'application/json'}

    def run(model, prompt):
        input = {
            "messages": [
            { "role": "system", "content": "You are a friendly medical assistant" },
            { "role": "user", "content": prompt }
            ]
        }
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
        return response.json()

    output = run("@cf/meta/llama-2-7b-chat-int8", question)
    print(output)
    return output["result"]["response"]

def save_to_doc(conversation):
    doc = docx.Document()
    doc.add_heading("Chatbot Conversation", level=1)

    for user, bot in conversation:
        p_user = doc.add_paragraph()
        p_user.add_run("User: ").bold = True
        p_user.add_run(user)

        p_bot = doc.add_paragraph()
        p_bot.add_run("Bot: ").bold = True
        p_bot.add_run(bot)

    doc.save("chatbot_conversation.docx")

def runner():

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    user_input = st.chat_input(placeholder="Your message")

    if user_input:
        if user_input:
            bot_reply = bot_response(user_input)
            st.session_state.conversation.append((user_input, bot_reply))
        else:
            st.warning("Please enter a question.")
        
        save_to_doc(st.session_state.conversation)

    st.text("Conversation History:")
    for user, bot in st.session_state.conversation:
        text = st.chat_message("User")
        message = st.chat_message("Assistant")
        text.write(user)
        message.write(bot)
    
    if st.button("End Conversation"):
        st.session_state.conversation=[]
        st.session_state.knowledge=""
        st.session_state.first_run = True
        st.snow()
        st.success("Click on any button to refresh", icon='✅')
        return
    
    st.download_button(
                label="Download Conversation",
                data=open("chatbot_conversation.docx", "rb").read(),
                file_name="Conversation.docx",
                mime="application/octet-stream",
                help="Click to download the conversation."
            )

cystcauses = """
It's not clear what causes simple kidney cysts. One theory suggests that kidney cysts develop when the surface layer of the kidney weakens and forms a pouch. The pouch then fills with fluid, detaches and develops into a cyst.
"""
cystsymptoms = """
Simple kidney cysts rarely cause trouble, but growing giants can stir. If a cyst balloons, expect lurking aches in your back or side, feverish whispers, or pangs in your upper abdomen. Don't wait for a chorus of complaints - consult a doctor if any solo symptom starts singing too loud.
"""
cysttreat = """
If symptomatic, treatment for a simple kidney cyst may involve piercing and draining with a scarring solution, using a thin needle to drain and shrink the cyst, or surgery for larger cysts. Surgery is uncommon for simple cysts but may be considered for complex cysts with potential cancerous changes.
"""

stonecauses = """Kidney stones often have no definite, single cause, although several factors may increase your risk. Kidney stones form when your urine contains more crystal-forming substances — such as calcium, oxalate and uric acid — than the fluid in your urine can dilute. At the same time, your urine may lack substances that prevent crystals from sticking together, creating an ideal environment for kidney stones to form."""

stonesymptoms = """Kidney stones are often asymptomatic until they move within the kidney or into the ureters. If lodged, they can cause severe pain, block urine flow, and lead to symptoms like abdominal and groin pain, painful urination, and more. Additional signs may include discolored urine, cloudy or foul-smelling urine, increased frequency, nausea, vomiting, and fever if infection is present. The pain's location and intensity may vary as the stone progresses through the urinary tract.
"""
stonetreat = """
Kidney stones may require treatments like shock wave lithotripsy (ESWL) or surgery, depending on size and complications. ESWL uses sound waves to break stones, lasting 45-60 minutes, with potential side effects. Surgery options include percutaneous nephrolithotomy for large stones and ureteroscopy for smaller ones. In cases of calcium phosphate stones due to hyperparathyroidism, surgery addresses gland issues or associated conditions to prevent stone formation.
"""

tumorcauses = """
It's not clear what causes most kidney cancers. 
Doctors know that kidney cancer begins when some kidney cells develop changes (mutations) in their DNA. A cell's DNA contains the instructions that tell a cell what to do. The changes tell the cells to grow and divide rapidly. The accumulating abnormal cells form a tumor that can extend beyond the kidney. Some cells can break off and spread (metastasize) to distant parts of the body."""

tumorsymptoms = """Early-stage kidney cancer often lacks noticeable symptoms. Over time, signs like blood in urine, persistent back/side pain, appetite loss, weight loss, fatigue, and fever may emerge.
"""
tumortreat = """For most kidney cancers, surgery is the primary treatment, aiming to remove the cancer while preserving kidney function. Surgical options include radical nephrectomy, removing the entire kidney, and partial nephrectomy, removing the tumor and a small margin of surrounding healthy tissue. Both procedures can be performed through open, laparoscopic, or robotic-assisted approaches.
"""
st.markdown(
    """
        <style>
            [data-testid="stSidebarNav"] {
                background-repeat: no-repeat;                
            }
            [data-testid="stSidebarNav"]::before {
                content: "MedAIgnosis";
                margin-left: 20px;
                margin-top: 20px;

                font-size: 30px;
                text-align: center;
                position: relative;
            }
        </style>
        """,
    unsafe_allow_html=True,
)
st.title("HealthOracle")
st.text(
    "Upload an image of a close up of your CT scan and we will tell you what is the disease you are suffering from"
)
# read images.zip as a binary file and put it into the button
with open("test.zip", "rb") as fp:
    btn = st.download_button(
        label="Download test images",
        data=fp,
        file_name="test.zip",
        mime="application/zip",
    )
image = st.file_uploader(
    "Upload Image", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=False
)

if image is not None:
    disp = False
    
    with image:
        st.image(image, caption="Your CT Scan", width=350)
        image_data = image.read()
        results = predictor.classify_image("748d2598-c0ce-481d-8e75-6a0d65dd5fdc", "Iteration1", image_data)
    disp = True
    
    c = st.image("loader.gif")
    time.sleep(3)
    c.empty()
    # Process and display the results
    if results.predictions:
        st.subheader("Prediction Results:")
        name="unknown"
        predict=0
        for prediction in results.predictions:
            if prediction.probability > predict and prediction.probability > 0.5:
                predict = prediction.probability
                name = prediction.tag_name

    if name!="unknown":
        st.text(f"Detected Kidney {name} with high confidence")
        if name == "Cyst":
            st.write(
                """
                Kidney cysts are round pouches of fluid that form on or in the kidneys. Kidney cysts can occur with disorders that may impair kidney function. But more often, kidney cysts are a type called simple kidney cysts. Simple kidney cysts aren't cancer and rarely cause problems.
                """
            )
            st.image("images/cyst.png", caption="Glioma", width=350)
            st.write("More Info")

            tab1, tab2, tab3 = st.tabs(
                ["Causes", "Symptoms", "Treatment"]
            )
            with tab1:
                st.write(cystcauses)
                st.write(
                    "More Info can be found on the [Mayo clinic website](https://www.mayoclinic.org/diseases-conditions/glioma/symptoms-causes/syc-20350251)"
                )
            with tab2:
                st.write(cystsymptoms)
                st.write(
                    "More Info can be found on the [Mayo clinic website](https://www.mayoclinic.org/diseases-conditions/glioma/symptoms-causes/syc-20350251)"
                )
            with tab3:
                st.write(cysttreat)
                st.write(
                    "More Info can be found on the [Mayo clinic website](https://www.mayoclinic.org/diseases-conditions/glioma/symptoms-causes/syc-20350251)"
                )
            
            st.markdown("##### Need more information? :speech_balloon:", unsafe_allow_html=False)
            first_run = st.session_state.get("first_run", True)

            if first_run:
                if st.button("Chat with AI Bot"):
                    st.session_state.first_run = False
                    runner()
            else:
                runner()
            
            doctor()

        elif (
            name == "Stone"
        ):
            st.write(
                """
                Kidney stones (also called renal calculi, nephrolithiasis or urolithiasis) are hard deposits made of minerals and salts that form inside your kidneys. Passing kidney stones can be quite painful, but the stones usually cause no permanent damage if they're recognized in a timely fashion.
                """
            )
            col1, col2=st.columns(2)
            col1.image("images/male_stone.png", caption="mstone", width=350)
            col2.image("images/female_stone.png", caption="fstone", width=350)
            st.write("Known Carried Diseases")
            btab1, btab2, btab3 = st.tabs(
                ["Causes", "Symptoms", "Treatment"]
            )
            with btab1:
                st.write(stonecauses)
                st.write(
                    "More Info can be found on the [Cancer Website](https://www.cancer.gov/rare-brain-spine-tumor/tumors/meningioma)"
                )
            with btab2:
                st.write(stonesymptoms)
                st.write(
                    "More Info can be found on the [Cancer Website](https://www.cancer.gov/rare-brain-spine-tumor/tumors/meningioma)"
                )
            with btab3:
                st.write(stonetreat)
                st.write(
                    "More Info can be found on the [Cancer Website](https://www.cancer.gov/rare-brain-spine-tumor/tumors/meningioma)"
                )
            
            st.markdown("##### Need more information? :speech_balloon:", unsafe_allow_html=False)
            first_run = st.session_state.get("first_run", True)

            if first_run:
                if st.button("Chat with AI Bot"):
                    st.session_state.first_run = False
                    runner()
            else:
                runner()
            doctor()

        elif name == "Tumor":
            st.write(
                """
                Kidney cancer is cancer that begins in the kidneys. Your kidneys are two bean-shaped organs, each about the size of your fist. They're located behind your abdominal organs, with one kidney on each side of your spine.

                In adults, renal cell carcinoma is the most common type of kidney cancer. Other less common types of kidney cancer can occur. Young children are more likely to develop a kind of kidney cancer called Wilms' tumor.
                """
            )
            st.image("kidneycancer.png", caption="Kidney Cancer", width=350)
            st.write("Known Carried Diseases")
            ctab1, ctab2, ctab3 = st.tabs(
                ["Causes", "Symptoms", "Treatment"]
            )
            with ctab1:
                st.write(tumorcauses)
                st.write(
                    "More Info can be found on the [MAYO clinic website](https://www.mayoclinic.org/diseases-conditions/pituitary-tumors/symptoms-causes/syc-20350548)"
                )
            with ctab2:
                st.write(tumorsymptoms)
                st.write(
                    "More Info can be found on the [MAYO clinic website](https://www.mayoclinic.org/diseases-conditions/pituitary-tumors/symptoms-causes/syc-20350548)"
                )
            with ctab3:
                st.write(tumortreat)
                st.write(
                    "More Info can be found on the [MAYO clinic website](https://www.mayoclinic.org/diseases-conditions/pituitary-tumors/symptoms-causes/syc-20350548)"
                )
            
            st.markdown("##### Need more information? :speech_balloon:", unsafe_allow_html=False)
            first_run = st.session_state.get("first_run", True)

            if first_run:
                if st.button("Chat with AI Bot"):
                    st.session_state.first_run = False
                    runner()
            else:
                runner()

            doctor()

    else:
        st.text("Feel Safe! No disease detected")
    
