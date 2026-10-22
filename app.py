import streamlit as st
import resend

st.set_page_config(page_title="Simple Mailer", layout="centered")
st.title("Simple Mailer (via Resend API)")

# --- Configuration (use st.secrets in production) ---
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Resend API Key", type="password")
sender_email = st.sidebar.text_input("Sender Email", value="onboarding@resend.dev")

if api_key:
    resend.api_key = api_key

# --- Email Form ---
st.header("Compose Email")
reply_to = st.text_input("Reply-To Address")
recipient = st.text_input("Recipient Email")
subject = st.text_input("Subject")
body = st.text_area("Message Body", height=200)

if st.button("Send Email"):
    if not all([api_key, sender_email, recipient, subject, body]):
        st.error("Please fill in all fields.")
    else:
        try:
            params = {
                "from": sender_email,
                "to": [recipient],
                "subject": subject,
                "html": f"<p>{body.replace(chr(10), '<br>')}</p>",
            }
            if reply_to:
                params["reply_to"] = reply_to

            email = resend.Emails.send(params)
            st.success(f"Email sent! ID: {email['id']}")
        except Exception as e:
            st.error(f"Failed: {e}")