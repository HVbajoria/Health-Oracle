import streamlit as st
import time
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import requests

doctors = [
    {
        "name": "Dr. Harshavardhan Bajoria",
        "specialization": "Pulmonologist",
        "location": "Kolkata",
        "available_days": "Mon, Tue, Fri",
        "contact": "hvbajoria@hotmail.com",
    },
    {
        "name": "Dr. Soumya Upadhyay",
        "specialization": "Chest Physician",
        "location": "Mumbai",
        "available_days": "Wed, Thu, Sat",
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