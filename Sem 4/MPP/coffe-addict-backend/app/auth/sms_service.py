import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
    raise ValueError(f"Twilio credentials are not properly configured: {TWILIO_ACCOUNT_SID}, {TWILIO_AUTH_TOKEN}, {TWILIO_PHONE_NUMBER}")

# In-memory storage for 2FA codes (job_id -> code_data)
# TODO: In production, replace this with Redis or a database table for better persistence and scalability
# Keys: job_id
# Values: {
#   code: str,             # 6-digit verification code
#   phone_number: str,     # User's phone number
#   username: str,         # User's username for completing login
#   created_at: datetime,  # When the code was created
#   expires_at: datetime,  # When the code expires (5 minutes after creation)
#   attempts: int,         # Number of verification attempts
#   message_sid: str       # Twilio message ID
# }
verification_codes: Dict[str, dict] = {}

class SMSService:
    def __init__(self):
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            raise ValueError("Twilio credentials are not properly configured")
        
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.from_number = TWILIO_PHONE_NUMBER

    def generate_verification_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))

    def generate_job_id(self) -> str:
        """Generate a unique job ID"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    def send_verification_code(self, phone_number: str, username: str = None) -> str:
        """
        Send a verification code to the phone number
        Returns the job_id for verification
        """
        self._clean_expired_codes()
        
        code = self.generate_verification_code()
        job_id = self.generate_job_id()
        
        if not phone_number.startswith('+') and not phone_number.startswith('00'):
            phone_number = f"+1{phone_number}"
        
        try:
            message = self.client.messages.create(
                body=f"Your Coffee Addict verification code is: {code}. This code expires in 5 minutes.",
                from_=self.from_number,
                to=phone_number
            )
            
            verification_codes[job_id] = {
                'code': code,
                'phone_number': phone_number,
                'username': username,
                'created_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(minutes=5),
                'attempts': 0,
                'message_sid': message.sid
            }
            
            return job_id
            
        except Exception as e:
            raise Exception(f"Failed to send SMS: {str(e)}")

    def verify_code(self, job_id: str, submitted_code: str) -> bool:
        """
        Verify the submitted code against the job_id
        Returns True if valid, False otherwise
        Removes the job_id from storage after verification attempt
        """
        # Clean expired codes first
        self._clean_expired_codes()
        
        if job_id not in verification_codes:
            return False
        
        code_data = verification_codes[job_id]
        
        # Check if code is expired
        if datetime.utcnow() > code_data['expires_at']:
            del verification_codes[job_id]
            return False
        
        # Increment attempts
        code_data['attempts'] += 1
        
        # Check if too many attempts (optional security measure)
        if code_data['attempts'] > 3:
            del verification_codes[job_id]
            return False
        
        # Verify code
        is_valid = code_data['code'] == submitted_code
        
        # If valid or max attempts reached, remove from storage
        if is_valid or code_data['attempts'] >= 3:
            del verification_codes[job_id]
        
        return is_valid

    def _clean_expired_codes(self):
        """Remove expired verification codes from memory"""
        current_time = datetime.utcnow()
        expired_jobs = [
            job_id for job_id, data in verification_codes.items()
            if current_time > data['expires_at']
        ]
        
        for job_id in expired_jobs:
            del verification_codes[job_id]

    def get_verification_status(self, job_id: str) -> Optional[dict]:
        """Get status of a verification job"""
        self._clean_expired_codes()
        
        if job_id not in verification_codes:
            return None
        
        code_data = verification_codes[job_id]
        return {
            'job_id': job_id,
            'phone_number': code_data['phone_number'][-4:],  # Only show last 4 digits
            'created_at': code_data['created_at'],
            'expires_at': code_data['expires_at'],
            'attempts': code_data['attempts']
        }

    def get_username_from_job(self, job_id: str) -> Optional[str]:
        """Get username associated with a verification job"""
        self._clean_expired_codes()
        
        if job_id not in verification_codes:
            return None
        
        return verification_codes[job_id].get('username')

# Create a singleton instance
sms_service = SMSService()
__all__ = ['sms_service']
