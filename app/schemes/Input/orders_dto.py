from typing import  Optional
from pydantic import BaseModel, Field
from datetime import datetime

class OrderDetail_InputDTO(BaseModel):
    Cantidad : int = Field(..., description="Quantity per product")        
    ValorItemTotal: float = Field(..., description="Total Order value")     
    ValorItemSinImpuestos: float = Field(..., description="Total Order value")  
    FechaCurso: Optional[datetime] = Field(default=None, description="Course date")
    Sku: int = Field(..., description="product identifier")  

class DigitalCard_InputDTO(BaseModel):
    name: str = Field(..., description="Cardholder's name")
    email: str = Field(..., description="Cardholder's email")
    phone: str = Field(..., description="Cardholder's phone number")
    service: str = Field(..., description="Service offered")
    city: str = Field(..., description="Cardholder's city")
    address: str = Field(..., description="Cardholder's address")
    website: str = Field(..., description="Cardholder's website")
    facebook: str = Field(..., description="Facebook profile")
    instagram: str = Field(..., description="Instagram profile")

class Order_InputDTO(BaseModel):
    Nit: str = Field(..., description="Customer Company nit")
    EmailComprador: str = Field(..., description="Customer company mail") 
    ValorOrdenTotal: float = Field(..., description="Total Order value") 
    ValorOrdenSinImpuestos: float = Field(..., description="Order value before taxes") 
    OrdenDetalles: Optional[list[OrderDetail_InputDTO]] = Field(default=[], description="Order detail") 
    VtexOC: str = Field(..., description="Purchase order number")
    EmailTeleventas: str = Field(..., description="Salesman email")
    Sponsor: Optional[str] = Field(default=None, description="RVC program sponsor")
    Digital_cards: Optional[list[DigitalCard_InputDTO]] = Field(default=[], description="Digital cards data") 
