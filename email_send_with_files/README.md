# Email Sender with Attachments

This project sends an email with attachment files via Gmail SMTP using a small Flask API.

## Project structure

- `main.py` - Flask app that sends an email with attachments.
- `requirements.txt` - Python dependencies.
- `Dockerfile` - container configuration for deployment.
- `attachments/` - folder containing demo attachment files.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables for your sender and receiver email.

Required:

- `SENDER_EMAIL_1`
- `APP_PASSWORD_1`
- `RECEIVER_EMAIL`

Optional second sender:

- `SENDER_EMAIL_2`
- `APP_PASSWORD_2`

3. Run the app:

```bash
python main.py
```

The app listens on port `8080` by default.

## Send a demo email

Use `curl` or a similar HTTP client:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"sender":"1"}' http://localhost:8080/
```

This will send an email with:

- `attachments/ProfessionalDataEngineer.pdf`
- `attachments/Associate Cloud Engineer Certification.jpg`

## Notes

- The app sends two attachments: one PDF and one JPG.
- Attachments are loaded from the `attachments/` folder.
- You can change the subject/body or add more attachments in `main.py`.
