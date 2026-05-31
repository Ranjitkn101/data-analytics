import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request

app = Flask(__name__)

@app.post("/")
def send_email():

    data = request.get_json(silent=True) or {}
    sender_choice = str(data.get("sender", "1"))

    sender = os.environ[f"SENDER_EMAIL_{sender_choice}"]
    password = os.environ[f"APP_PASSWORD_{sender_choice}"]
    receiver = os.environ["RECEIVER_EMAIL"]

    # Gmail SMTP (same for both senders)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "Demo Email with Attachments"

    body = (
        "Hello,\n\n"
        "This is a simple demo email with two attachments.\n\n"
        "Best regards,\n"
        "Demo Sender"
    )

    attachments = [
        os.path.join("attachments", "ProfessionalDataEngineer.pdf"),
        os.path.join("attachments", "Associate Cloud Engineer Certification.jpg"),
    ]

    missing_files = [path for path in attachments if not os.path.isfile(path)]
    if missing_files:
        return f"Attachment file(s) not found: {', '.join(missing_files)}", 400

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for file_path in attachments:
        with open(file_path, "rb") as f:
            payload = f.read()

        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == ".pdf":
            maintype, subtype = "application", "pdf"
        elif file_ext in [".jpg", ".jpeg"]:
            maintype, subtype = "image", "jpeg"
        else:
            maintype, subtype = "application", "octet-stream"

        part = MIMEBase(maintype, subtype)
        part.set_payload(payload)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
        msg.attach(part)

    # Gmail SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

    return f"Email sent successfully using sender {sender_choice}!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
