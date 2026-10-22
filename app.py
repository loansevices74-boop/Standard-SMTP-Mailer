import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(page_title="Simple Mailer", layout="centered")
st.title("Standard SMTP Mailer")

# Sidebar for SMTP Configuration
st.sidebar.header("SMTP Configuration")
smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP Port", value=587, step=1)
sender_email = st.sidebar.text_input("Sender Email")
# Note: In production, use st.secrets or environment variables for passwords.
sender_password = st.sidebar.text_input("Sender Password / App Password", type="password")

# Main form for Email Content
st.header("Compose Email")
reply_to = st.text_input("Reply-To Address")
recipient_email = st.text_input("Recipient Email")
subject = st.text_input("Subject")
body = st.text_area("Message Body", height=200)

if st.button("Send Email"):
    if not all([sender_email, sender_password, recipient_email, subject, body]):
        st.error("Please fill in all required fields.")
    else:
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            if reply_to:
                msg['Reply-To'] = reply_to
            
            msg.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server and send
            # Using TLS for secure connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() 
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")