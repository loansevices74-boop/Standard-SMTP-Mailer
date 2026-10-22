import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(page_title="Brevo Mailer", layout="centered")
st.title("📧 Simple Brevo Mailer")

# --- Configuration ---
st.sidebar.header("Brevo Configuration")
# In production, this should come from st.secrets["BREVO_API_KEY"]
api_key = st.sidebar.text_input("Brevo API Key", type="password", help="Get this from your Brevo dashboard")
sender_email = st.sidebar.text_input("Sender Email", help="Must be verified in your Brevo account")
sender_name = st.sidebar.text_input("Sender Name", value="My App")

# --- Email Form ---
st.header("Compose Email")
col1, col2 = st.columns(2)
with col1:
    recipient = st.text_input("Recipient Email")
with col2:
    reply_to = st.text_input("Reply-To Address (Optional)")

subject = st.text_input("Subject")
body = st.text_area("Message Body (HTML supported)", height=200, value="<p>Hello,<br>This is a test email sent via Streamlit and Brevo.</p>")

if st.button("Send Email", type="primary"):
    if not all([api_key, sender_email, recipient, subject, body]):
        st.error("⚠️ Please fill in all required fields (API Key, Sender, Recipient, Subject, Body).")
    else:
        with st.spinner("Sending email..."):
            # Brevo API Endpoint
            url = "https://api.brevo.com/v3/smtp/email"
            
            # Headers
            headers = {
                "accept": "application/json",
                "api-key": api_key,
                "content-type": "application/json"
            }
            
            # Payload
            payload = {
                "sender": {
                    "email": sender_email,
                    "name": sender_name
                },
                "to": [
                    {
                        "email": recipient
                    }
                ],
                "subject": subject,
                "htmlContent": body
            }
            
            # Add Reply-To only if provided
            if reply_to:
                payload["replyTo"] = {"email": reply_to}

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status() # Raises an error for bad status codes (4xx, 5xx)
                
                st.success("✅ Email sent successfully!")
                st.json(response.json()) # Shows the Brevo message ID
                
            except requests.exceptions.HTTPError as errh:
                st.error(f"❌ HTTP Error: {errh}")
                st.json(response.json()) # Brevo usually returns a helpful error message here
            except requests.exceptions.ConnectionError as errc:
                st.error(f"❌ Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                st.error(f"❌ Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                st.error(f"❌ Something went wrong: {err}")