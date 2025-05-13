from http.client import HTTPException
import os
import requests
import base64
import json
from dtos import KYCFullDataDTO

class DiditCore:
    """
    Core class for DIDIT module.
    """

    def __init__(self):
        self.auth_url = "https://apx.didit.me"
        self.verification_url = "https://verification.didit.me"
        self.__KYC_API_FEATURES = os.getenv("DIDIT_API_FEATURES")
        self.__KYC_CLIENT_ID = os.getenv("DIDIT_CLIENT_ID")
        self.__KYC_CLIENT_SECRET = os.getenv("DIDIT_CLIENT_SECRET")
        self.__KYC_CALLBACK_URL = os.getenv("KYC_CALLBACK_URL")
        self.__access_token = None
    
    def __encoded_credentials(self):
        """
        Encode the credentials in base64.
        """
        client_id = self.__KYC_CLIENT_ID
        client_secret = self.__KYC_CLIENT_SECRET
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return encoded_credentials
    
    def authenticate(self):
      """
      Authenticate with the didit API and get the access token.
      """
      encoded_credentials = self.__encoded_credentials()
      # Setting headers for the request
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Authorization': f"Basic {encoded_credentials}"
      }
      payload = {
        'grant_type': 'client_credentials'
      }
      # Making the request to the API
      try:
        response = requests.post(f'{self.auth_url}/auth/v2/token/', headers=headers, data=payload, timeout=10)
        # Check if the response is successful
        response.raise_for_status()  
        # Parse the JSON response
        token_response = response.json()
      
        if not token_response:  
          raise EnvironmentError("KYC MANAGER: Failed to obtain authentication token.")
        
        self.__access_token = token_response.get('access_token')

      except Exception as e:
        raise HTTPException(f"KYC MANAGER: HTTP {response.status_code}: {response.text}") 
  
    
    def create_verification_session(self, user_email:str):
      """
      Create the verification session and get verification URL.
      """
      if not user_email:
        raise EnvironmentError("KYC MANAGER: A user ID or email is required to start the verification session.")
      headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.__access_token}"
      }
      payload = {
        'callback': self.__KYC_CALLBACK_URL,
        'features': self.__KYC_API_FEATURES,
        'vendor_data': user_email
      }
      
      # Making the request to the API
      try:
        response = requests.post(f'{self.verification_url}/v1/session/', headers=headers, json=payload)
        response.raise_for_status()  
        session = response.json()
        if not session:  
            return None
        return self.__parse_initial_session_data(session)

      except Exception as e:
        raise HTTPException(f"KYC MANAGER: HTTP {response.status_code}: {response.text}") 
  
        
    def retrieve_session(self, session_id):
      """
      Retrieve the session information.
      """
      if not session_id:
        raise EnvironmentError("KYC MANAGER: A session ID is required to retrieve the session information.")
      
      # Setting headers for the request 
      headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.__access_token}"
      }
      # Making the request to the API
      try:
        response = requests.get(f'{self.verification_url}/v1/session/{session_id}/decision/', headers=headers)
        response.raise_for_status()  
        session = response.json()
        if not session:  
            return None
        return self.__parse__full_session_data(session)  

      except Exception as e:
        raise HTTPException(f"KYC MANAGER: HTTP {response.status_code}: {response.text}") 
    
    
    
    def __parse__full_session_data(self, session):
      """
      Parse the session information and return a KYCDataDTO object.
      """
      if not session:
        raise EnvironmentError("KYC MANAGER: A session is required to parse the session information.")
      
      if "kyc" in session:
        decision = session.get("kyc")
        if decision:
          location = session.get("location")
          kyc_data = KYCFullDataDTO(
              provider = "DIDIT",
              session_id = session.get("session_id"),
              session_url = session.get("session_url"),
              status = session.get("status"),
              kyc_verify_types = session.get("features"),
              vendor_data = session.get("vendor_data"),
              document_type = decision.get("document_type"),
              document_number = decision.get("document_number"),
              personal_number= decision.get("personal_number"),
              portrait_image = decision.get("portrait_image"),
              front_image = decision.get("front_image"),
              back_image = decision.get("back_image"),
              expiration_date = decision.get("expiration_date"),
              date_of_issue = decision.get("date_of_issue"),
              is_nfc_verified = decision.get("is_nfc_verified"),
              issuing_state = decision.get("issuing_state"),
              issuing_state_name = decision.get("issuing_state_name"),
              first_name = decision.get("first_name"),
              last_name = decision.get("last_name"),
              full_name = decision.get("full_name"),
              epassport_status = decision.get("epassport_status"),
              address = decision.get("address"),
              gender = decision.get("gender"),
              date_of_birth = decision.get("date_of_birth"),
              marital_status = decision.get("marital_status"),
              nationality = decision.get("nationality"),
              ip_country = location.get("ip_country"),
              ip_country_code = location.get("ip_country_code"),
              created_at = decision.get("created_at"),
            )
          return kyc_data.to_dict()
        else:
          kyc_data = KYCFullDataDTO(
            provider = "DIDIT",
            session_id = session.get("session_id"),
            session_url = session.get("session_url"),
            status = session.get("status"),
            kyc_verify_types = session.get("features"),
            vendor_data = session.get("vendor_data"),
          )
          return kyc_data.to_dict()
          

    def __parse_initial_session_data(self, session):
      """
      Parse the session information and return a KYCDataDTO object.
      """
      if not session:
        raise EnvironmentError("KYC MANAGER: A session is required to parse the session information.")
    
      kyc_data = KYCFullDataDTO(
        provider = "DIDIT",
        session_id = session.get("session_id"),
        session_url = session.get("url"),
        status = session.get("status"),
        kyc_verify_types = session.get("features"),
        vendor_data = session.get("vendor_data"),
      )
      return kyc_data.to_dict()