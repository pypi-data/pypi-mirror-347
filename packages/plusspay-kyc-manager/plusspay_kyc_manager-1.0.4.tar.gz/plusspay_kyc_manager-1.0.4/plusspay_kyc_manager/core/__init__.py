import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from didit.didit_core import DiditCore

class PlusspayKYCManager:
  
    def __init__(self):
        self.name = "Plusspay KYC Manager"
        self.description = "Core module for Plusspay KYC Manager"
        self.version = "1.0.0"
        self.author = "Plusspay"
        self.license = "MIT"
        self.license_url = "https://opensource.org/licenses/MIT"
        self.providers = ['DIDIT', 'METAMASK']
        self.__KYC_PROVIDER = ""
        self.__KYC_API_FEATURES= ""
        self.__KYC_CLIENT_ID = ""
        self.__KYC_CLIENT_SECRET = ""
        self.__KYC_CALLBACK_URL = ""
        self.__didit_instance = None

    def get_full_info(self):  
      return {
          "name": self.name,
          "description": self.description,
          "version": self.version,
          "author": self.author,
          "license": self.license,
          "license_url": self.license_url,
          "Current KYC Provider": self.__KYC_PROVIDER,
          "KYC API Features configured": self.__KYC_API_FEATURES,
      }
        
    def __check_environment(self):
      """
      Check if the environment vars is set up correctly.
      """
        
      self.__KYC_PROVIDER = os.getenv("KYC_PROVIDER")
      self.__KYC_API_FEATURES = os.getenv("DIDIT_API_FEATURES")
      self.__KYC_CLIENT_ID = os.getenv("DIDIT_CLIENT_ID")
      self.__KYC_CLIENT_SECRET = os.getenv("DIDIT_CLIENT_SECRET")
      self.__KYC_CALLBACK_URL = os.getenv("KYC_CALLBACK_URL")
  
      if not self.__KYC_PROVIDER:
        raise EnvironmentError("KYC MANAGER: KYC_PROVIDER is not set, the environment for the KYC manager is not set correctly.")
      
      if self.__KYC_PROVIDER not in self.providers:
        raise EnvironmentError("KYC MANAGER: KYC_PROVIDER is not valid.")
      
      if not self.__KYC_CALLBACK_URL:
          raise EnvironmentError("KYC MANAGER: KYC_CALLBACK_URL is not set, the environment for the KYC manager is not set correctly.")
        
      if self.__KYC_PROVIDER == "DIDIT":
        if not self.__KYC_API_FEATURES:
          raise EnvironmentError("KYC MANAGER: KYC_API_FEATURES is not set, the environment for the KYC manager is not set correctly.")
        if not self.__KYC_CLIENT_ID:
          raise EnvironmentError("KYC MANAGER: KYC_CLIENT_ID is not set, the environment for the KYC manager is not set correctly.")
        if not  self.__KYC_CLIENT_SECRET:
          raise EnvironmentError("KYC MANAGER: KYC_CLIENT_SECRET is not set, the environment for the KYC manager is not set correctly.")
        if not self.__KYC_API_FEATURES:
          raise EnvironmentError("KYC MANAGER: KYC_API_FEATURES is not set for DIDIT provider.")
       

    def set_environment(self):
        """
        Start a session for the KYC manager.
        """
        self.__check_environment()
        
        if self.__KYC_PROVIDER == "DIDIT":
            # Initialize the DIDIT provider
            self.__didit_instance = DiditCore()
            self.__didit_instance.authenticate()
        elif self.__KYC_PROVIDER == "METAMASK":
            # Initialize the other provider
            pass
      
    def create_session(self, user_email:str):
        """
        Start a session for the KYC manager.
        """
        self.__check_environment()
        
        if self.__KYC_PROVIDER == "DIDIT":
            # Initialize the DIDIT provider
            return self.__didit_instance.create_verification_session(user_email)
        elif self.__KYC_PROVIDER == "METAMASK":
            # Initialize the other provider
            pass
    
    def get_session_data(self, session_id:str):
        """
        Create a session for the KYC manager.
        """
        if not session_id:
            raise EnvironmentError("KYC MANAGER: A session ID is required to start the verification session.")
          
        self.__check_environment()
        
        if self.__KYC_PROVIDER == "DIDIT":
            # Initialize the DIDIT provider
            data = self.__didit_instance.retrieve_session(session_id)
            return data
        elif self.__KYC_PROVIDER == "METAMASK":
            # Initialize the other provider
            pass