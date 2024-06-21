from pydantic import BaseModel
from typing import Literal
 

class ProcessA1Response(BaseModel):
    ad_description: str
    ad_purpose: Literal["BRAND-BUILDING", "CONVERSION"]

class ProcessA2Response(BaseModel):
    saliency_description: str

class ProcessBResponse(BaseModel):
    cognitive_description: str

class ProcessCResponse(BaseModel):
    ad_description: str
    ad_purpose: str
    saliency_description: str
    cognitive_description: str