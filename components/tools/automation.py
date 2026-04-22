import os
import subprocess
import tempfile
import smtplib
import urllib.parse
import requests
from typing import List, Optional, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from components.config import Config

def run_python_script(code: str) -> Dict[str, str]:
    """Execute a Python script safely in a temporary file and return its output."""
    print("\n" + "="*30)
    print("🚀 PYTHON SCRIPT EXECUTION REQUESTED")
    print("-" * 30)
    print(code)
    print("="*30)
    
    confirm = input("\nDo you want to execute this script? (y/n): ").strip().lower()
    if confirm != 'y':
        return {"stdout": "", "stderr": "Execution cancelled by user."}

    print("\n[Tool Call] Executing run_python_script...")
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            file_path = f.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e)}

def send_email(
    receiver_email: str,
    subject: str,
    body: str,
    cc_emails: Optional[List[str]] = None,
    attachments: Optional[List[str]] = None,
) -> str:
    """Send an email using SMTP with optional CC and file attachments."""
    print("\n" + "="*30)
    print("📧 EMAIL SENDING REQUESTED")
    print(f"To: {receiver_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    if cc_emails: print(f"CC: {', '.join(cc_emails)}")
    if attachments: print(f"Attachments: {', '.join(attachments)}")
    print("="*30)

    confirm = input("\nDo you want to send this email? (y/n): ").strip().lower()
    if confirm != 'y':
        return "❌ Sending cancelled by user."

    print(f"\n[Tool Call] Sending email to {receiver_email}...")
    try:
        sender_email = Config.EMAIL
        sender_password = Config.EMAIL_PASS

        if not sender_email or not sender_password:
            return "❌ Email credentials not configured in environment."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        recipients = [receiver_email]
        if cc_emails:
            msg["Cc"] = ", ".join(cc_emails)
            recipients += cc_emails

        msg.attach(MIMEText(body, "plain"))

        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    return f"❌ File not found: {file_path}"
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(file_path)
                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(part)

        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg, from_addr=sender_email, to_addrs=recipients)
        server.quit()

        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Failed to send email: {e}"

def compile_latex_to_pdf(
    latex_code: str,
    output_file: str = "output.pdf",
    timeout: int = 30
) -> Optional[str]:
    """Compile LaTeX code into a PDF using LaTeX.Online free API."""
    print(f"\n[Tool Call] compile_latex_to_pdf -> {output_file}")
    try:
        base_url = "https://latexonline.cc/compile"
        encoded_latex = urllib.parse.quote(latex_code)
        url = f"{base_url}?text={encoded_latex}"
        
        response = requests.get(url, timeout=timeout)
        if response.status_code != 200:
            return f"❌ Failed to compile LaTeX. Status code: {response.status_code}"

        with open(output_file, "wb") as f:
            f.write(response.content)

        return f"✅ PDF successfully generated: {output_file}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
