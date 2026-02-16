import os
import requests
import logging

class EmailService:
    """
    Robust Email Service using Resend API.
    Bypasses Supabase SMTP limits by sending transactional emails directly.
    """
    
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY")
        self.api_url = "https://api.resend.com/emails"
        self.sender = "Haineo Security <security@haineo.ai>" # Or a verified domain if available, else standard
        # If user hasn't verified a domain in Resend, they must use "onboarding@resend.dev" to test, 
        # BUT this only works if sending TO the verified email. 
        # Given the user provided a key, we assume they might have a domain or are testing.
        # SAFE FALLBACK: If no domain, use a generic display name with the user's email if allowed, 
        # but Resend requires a verified domain.
        # Let's check if the user provided a specific sender in .env or default to onboarding.
        self.sender = os.getenv("EMAIL_SENDER", "onboarding@resend.dev") 

    def send_email(self, to_email, subject, html_content):
        if not self.api_key:
            print("// EmailService: No RESEND_API_KEY found.")
            return False

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "from": self.sender,
            "to": to_email,
            "subject": subject,
            "html": html_content
        }

        try:
            resp = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            if resp.status_code in [200, 201]:
                print(f"// EmailService: Email sent to {to_email}")
                return True
            else:
                print(f"// EmailService Error ({resp.status_code}): {resp.text}")
                return False
        except Exception as e:
            print(f"// EmailService Connection Error: {e}")
            return False

    def send_recovery_email(self, email, action_link):
        html = f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
            <h2>Reset Password Request</h2>
            <p>We received a request to reset your password for Haineo MT5.</p>
            <p>Click the link below to verify your identity and reset your password:</p>
            <p>
                <a href="{action_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Reset Password
                </a>
            </p>
            <p>Or copy this link: <br>{action_link}</p>
            <p>If you did not request this, please ignore this email.</p>
        </div>
        """
        return self.send_email(email, "Reset Your Password - Haineo", html)

    def send_magic_link(self, email, action_link):
        html = f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
            <h2>Your Magic Login Link</h2>
            <p>Click the button below to log in securely to Haineo MT5:</p>
            <p>
                <a href="{action_link}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Log In Now
                </a>
            </p>
            <p>Or copy this link: <br>{action_link}</p>
            <p>Valid for 15 minutes.</p>
        </div>
        """
        return self.send_email(email, "Secure Login Link - Haineo", html)
