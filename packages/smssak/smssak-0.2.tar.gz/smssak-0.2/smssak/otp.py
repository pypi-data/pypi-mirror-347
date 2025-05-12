import requests
from enum import Enum

class MessageType(Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"

def send_otp(country: str,  phone: str, project_id: str, message_type: str, key: str):
    """
    Sends an OTP to a phone number or whatsapp.
    
    :param country: The 2-letter country code (e.g., 'dz' for Algeria).
    :param phone: The phone number to send the OTP to.
    :param project_id: The project ID for your OTP service.
    :param message_type: The message type sms/whatsapp.
    :param key: The API key for authenticating the request.
    """
    url = 'https://sendotp-47lvvvrp4a-uc.a.run.app'
    headers = {
        'Content-Type': 'application/json',
        'key': key
    }
    data = {
        "country": country,
        "phone": phone,
        "projectId": project_id,
        "type": message_type
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.content

def verify_otp(country: str, phone: str, project_id: str, otp: str, key: str):
    """
    Verifies an OTP for a given phone number and project ID.
    
    :param country: The 2-letter country code (e.g., 'dz' for Algeria).
    :param phone: The phone number to verify.
    :param project_id: The project ID for the OTP verification service.
    :param otp: The OTP to verify.
    :param key: The API key for authenticating the request.
    """
    url = 'https://verifyotp-47lvvvrp4a-uc.a.run.app'
    headers = {
        'Content-Type': 'application/json',
        'key': key
    }
    data = {
        "country": country,
        "phone": phone,
        "projectId": project_id,
        "otp": otp
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def send_message(country: str, phone: str, project_id: str, message: str, key: str):
    """
    Sen message for  a given phone number and project ID.
    
    :param country: The 2-letter country code (e.g., 'dz' for Algeria).
    :param phone: The phone number to verify.
    :param project_id: The project ID for the OTP verification service.
    :param message: The message will be send.
    :param key: The API key for authenticating the request.
    """
    url = 'https://sendmessage-47lvvvrp4a-uc.a.run.app'
    headers = {
        'Content-Type': 'application/json',
        'key': key
    }
    data = {
        "country": country,
        "phone": phone,
        "projectId": project_id,
        "message": message
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
