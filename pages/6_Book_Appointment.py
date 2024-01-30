import streamlit as st
import time
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests
import streamlit.components.v1 as components
import js2py 
import sys

def book_appointment(doctor_name, patient_email, patient_name, textresponse):
    # Add your booking logic here, e.g., database integration, etc.


    # Send confirmation email to the patient
    send_confirmation_email(patient_email, doctor_name, patient_name, textresponse)


    # Send appointment email to the doctor
    doctor_email = get_doctor_email(doctor_name)
    send_appointment_email(doctor_email, patient_email, doctor_name, patient_name, textresponse)


    st.success(f"Appointment booked with {doctor_name}. You will be contacted soon!")


def send_confirmation_email(patient_email, doctor_name,patient_name, textresponse):
   # Replace 'your_azure_logic_app_url' with the URL of your Azure logic app to send appointment emails
    azure_logic_app_url = "https://prod-11.centralindia.logic.azure.com/workflows/a845897faa254f93a5db7375a917acc7/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qJUCl1H4fqe0QGHrhZQonWcYbCIM_W2Pv7sZElzdTLg"

    email_data = {
        "to": patient_email,
         "name": patient_name,
        "subject": "Appointment Confirmed at HealthOracle",
       
        "content": f"Your appointment with {doctor_name} has been booked successfully. You will be contacted soon.",
    }
    print(textresponse)

    response = requests.post(azure_logic_app_url, json=email_data)
    if response.status_code == 200 or response.status_code == 202:
        st.success("Confirmation email sent to the patient.")
    else:
        st.error("Failed to send confirmation email.")


def send_appointment_email(doctor_email, patient_email, doctor_name, patient_name, textresponse):
    # Replace 'your_azure_logic_app_url' with the URL of your Azure logic app to send appointment emails
    azure_logic_app_url ="https://prod-11.centralindia.logic.azure.com/workflows/a845897faa254f93a5db7375a917acc7/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qJUCl1H4fqe0QGHrhZQonWcYbCIM_W2Pv7sZElzdTLg"

    email_data = {
        "to": doctor_email,
        "name": doctor_name,
        "subject": "New Appointment at HealthOracle",
        "specialmessage": textresponse,
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
    for doctor in st.session_state.doctor:
        if doctor["name"] == doctor_name:
            return doctor["contact"]


def doctor():
    
    def gradient_text(text, color1, color2):
        gradient_css = f"""
        background: -webkit-linear-gradient(left, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 42px;
        """
        return f'<span style="{gradient_css}">{text}</span>'

    color1 = "#0d3270"
    color2 = "#0fab7b"
    text = "HealthOracle: Decode Your Health"
  
    # left_co, cent_co,last_co = st.columns(3)
    # with cent_co:
    #     st.image("images/logo.png", width=200)

    styled_text = gradient_text(text, color1, color2)
    st.write(f"<div style='text-align: center;'>{styled_text}</div>", unsafe_allow_html=True)
    st.markdown("### Book your appointment with ease")
    if "doctor" not in st.session_state:
        database_endpoint="https://hvbajoria101.kintone.com/k/v1/record.json?"
        database_headers={'X-Cybozu-API-Token':'LeX70V7wU3KdgKN6JkzOlLkLK8nShxoEFbuF1ZWj', 'Content-Type': 'application/json'}

        doctors = []

        # Fetching doctors from database
        for i in range(1,9):
            database_data = {
            'app':1,
            'id':i
            }

            database_response = requests.get(f"{database_endpoint}", headers=database_headers, json=database_data)
    
            doctor={}
            doctor["name"]=database_response.json()["record"]["Text"]["value"]
            doctor["specialization"]=database_response.json()["record"]["Text_0"]["value"]
            doctor["location"]=database_response.json()["record"]["Text_1"]["value"]
            doctor["available_days"]=database_response.json()["record"]["Text_3"]["value"]
            doctor["contact"]=database_response.json()["record"]["Text_2"]["value"]
            doctors.append(doctor)
        st.session_state.doctor = doctors

    if "treatment" in st.session_state:
        st.warning(f"We have detected: {st.session_state.treatment}\n", icon='📑')
    st.write("Select a doctor to view details and book an appointment: :stethoscope:")
    selected_doctor = st.selectbox("Select a doctor", [doctor["name"] for doctor in st.session_state.doctor])


    # Add an input field for the patient's email
    patient_email = st.text_input("Enter your email", "")
    patient_name = st.text_input("Enter your name", "")

    components.html("""<!DOCTYPE html> 
    <html lang="en"><head>
<script src="https://cdn.tiny.cloud/1/0jihkifpc837tensun96a5r8gkwpqi914vkk9f8in0gtxcve/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
</head><body>
<!-- Place the following <script> and <textarea> tags your HTML's <body> -->
<script>
  tinymce.init({
    selector: 'textarea',
    plugins: 'ai tinycomments mentions anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed permanentpen footnotes advtemplate advtable advcode editimage tableofcontents mergetags powerpaste tinymcespellchecker autocorrect a11ychecker typography inlinecss',
    toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | align lineheight | tinycomments | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
    mergetags_list: [
      { value: 'First.Name', title: 'First Name' },
      { value: 'Email', title: 'Email' },
    ],
    ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant")),
  });
</script>
<button onclick="content()">Get content</button>
<form method="post" action="somepage">
    <textarea id="myTextArea" class="mceEditor">I should buy a boat. </textarea>
</form>
<br><br>
<script type="text/javascript">

    tinyMCE.init({
        mode : "specific_textareas",
        editor_selector : "mceEditor"   //<<<---- 
    });
function content() {
    var contents = tinyMCE.get('myTextArea').getContent();
    const subdomain = 'hvbajoria101';
const apiToken = 'pK6weuGWDK6vLoayztUCzpc1MP3CRSemxB6vZsqN';

const url = `https://$hvbajoria101.kintone.com/k/v1/records.json`;

const data = {
  app: 2,
  records: [
    {
      Text: { value: content }
    }
  ]
};

fetch(url, {
  method: 'POST',
  headers: {
    'X-Cybozu-API-Token': apiToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(data => console.log('Response:', data))
  .catch(error => console.error('Error:', error));

}

</script>
</body></html>""")
    # code_2 = "src=\"" function get() {return tinymce.activeEditor.getContent();}"
    # textresponse = js2py.eval_js(code_2) 
    # print(textresponse())
    # from mycomponent import mycomponent
    # textresponse = mycomponent(my_input_value="hello there")
    
    if st.button("Book Appointment"):
        if not patient_email:
            st.warning("Please enter your email.")
        if not patient_name:
            st.warning("Please enter your name.")
        else:
            components.html("""<!DOCTYPE html> <html lang="en"><head>
            <script src="https://cdn.tiny.cloud/1/0jihkifpc837tensun96a5r8gkwpqi914vkk9f8in0gtxcve/tinymce/6/tinymce.min.js" referrerpolicy="origin">
            </script></head>
            <body>
            
            <script> tinyMCE.triggerSave();
            var myContent = tinymce.activeEditor.getContent();
            var body = {
  'app': 2,
  'record': {
    'Text': {
      'value': myContent
    }
  }
};
console.log(myContent)
kintone.api(kintone.api.url('/k/v1/record.json', true), 'POST', body, function(resp) {
  // success
  
  console.log(resp);
}, function(error) {
  // error
  console.log(error);
});</script>
            </body>""")

            # book_appointment(selected_doctor, patient_email, patient_name, textresponse)


    for doctor in st.session_state.doctor:
        if doctor["name"] == selected_doctor:
            st.subheader(doctor["name"])
            st.write(f"Specialization: {doctor['specialization']}")
            st.write(f"Location: {doctor['location']}")
            st.write(f"Available Days: {doctor['available_days']}")
st.markdown(
    """
        <style>
            [data-testid="stSidebarNav"] {
                background-repeat: no-repeat;                
            }
            [data-testid="stSidebarNav"]::before {
                content: "Health Oracle";
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
doctor()