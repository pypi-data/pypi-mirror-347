from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class KYCFullDataDTO:
    """
    Data Transfer Object for KYC (Know Your Customer) data.
    This class is used to transfer KYC data between different layers of the application.
    """
    provider: str = field(default="")
    session_id: str = field(default=None)
    session_url: Optional[str] = field(default="")
    status: str = field(default="Not Started")
    kyc_verify_types: str = field(default="")
    vendor_data: str = field(default="")
    ocr_status: Optional[str] = field(default="")
    document_type: Optional[str] = field(default="")
    document_number: Optional[str] = field(default="")
    personal_number: Optional[str] = field(default="")
    epassport_status: Optional[str] = field(default="")
    portrait_image: Optional[str] = field(default="")
    front_image: Optional[str] = field(default="")
    back_image: Optional[str] = field(default="")
    expiration_date: Optional[str] = field(default="")
    date_of_issue: Optional[str] = field(default="")
    is_nfc_verified: bool = field(default=False)
    issuing_state: Optional[str] = field(default="")
    issuing_state_name: Optional[str] = field(default="")
    face_match_status: Optional[str] = field(default="")
    ip_country: Optional[str] = field(default="")
    ip_country_code: Optional[str] = field(default="")
    created_at: Optional[str] = field(default="")
    # client data
    first_name: Optional[str] = field(default="")
    last_name: Optional[str] = field(default="")
    full_name: Optional[str] = field(default="")  
    gender: Optional[str] = field(default="")
    address: Optional[str] = field(default="")
    date_of_birth: Optional[str] = field(default="")
    marital_status:  Optional[str] = field(default="")
    nationality: Optional[str] = field(default="")
    

    def __str__(self):
        """
        Return a string representation of the KYCDataDTO instance.
        This is useful for debugging or logging purposes.
        """
        return f"KYCDataDTO(provider={self.provider}, session_id={self.session_id}, status={self.status}, document_number={self.document_number}, expiration_date={self.expiration_date}, date_of_issue={self.date_of_issue}, is_nfc_verified={self.is_nfc_verified}, issuing_state_code={self.issuing_state}, issuing_state_name={self.issuing_state_name}, face_match_status={self.face_match_status}, ip_country={self.ip_country}, ip_country_code={self.ip_country_code})"

    def to_dict(self):
        """
        Convert the KYCDataDTO instance to a dictionary.
        This is useful for serialization or sending data over the network.
        """
        
        return {
            "provider": self.provider,
            "session_id": self.session_id,
            "session_url": self.session_url,
            "status": self.status,
            "ocr_status": self.ocr_status,
            "epassport_status": self.epassport_status,
            "kyc_verify_types": self.kyc_verify_types,
            "vendor_data": self.vendor_data,
            "document_type": self.document_type,
            "personal_number": self.personal_number,
            "document_number": self.document_number,
            "portrait_image_url": self.portrait_image,
            "front_image_url": self.front_image,
            "back_image_url": self.back_image,
            "expiration_date": self.expiration_date,
            "date_of_issue": self.date_of_issue,
            "is_nfc_verified": self.is_nfc_verified,
            "issuing_state_code": self.issuing_state,
            "issuing_state_name": self.issuing_state_name,
            "face_match_status": self.face_match_status,
            "ip_country": self.ip_country,
            "ip_country_code": self.ip_country_code,
            "created_at": self.created_at,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "address": self.address,
            "date_of_birth": self.date_of_birth,
            "marital_status": self.marital_status,
            "nationality": self.nationality,
        }
        
      
   