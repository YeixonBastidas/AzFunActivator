from typing import List, Optional
from pydantic import BaseModel, Field

class DigitalCardDTO(BaseModel): 
      contact_name: str = Field(...) 
      contact_email: str = Field(...) 
      contact_mobile: str = Field(...) 
      offered_service_id:  int = Field(...) 
      city_id:  int = Field(...) 
      street: str = Field(...) 
      url_website: str = Field(...) 
      url_facebook: str = Field(...) 
      url_instagram: str = Field(...) 
      postulation_id: Optional[int] = Field(default=None)

class PostulationDTO(BaseModel):   
    nit_beneficiary: str = Field(...),
    nit_sponsor: str = Field(...),
    product_rvc:  int = Field(...),
    codes_quantity: int = Field(...),
    origin: str = Field(...),
    contact_email: str = Field(...),
    glns_codes_quantity: Optional[int] = Field(default=None),
    invoice_codes_quantity: Optional[int] = Field(default=None),   
    colabora_level: Optional[int] = Field(default=0),    
    digital_card_ids: Optional[List[DigitalCardDTO]] = Field(default=[])  
    crecemype_theme: Optional[str] =Field(default=None)


   