from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class CopyRequest(BaseModel):
    content_type: str
    audience: str
    product_info: str
    cta: bool
    
    tone_of_voice: Optional[str] = None
    style: Optional[str] = None
    brand_sample: Optional[str] = Field(default=None, max_length=3000)
    keywords: Optional[List[str]] = None
    
    @field_validator("content_type", "audience", "product_info")
    @classmethod
    def required_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty or whitespace")
        return v
    
    @field_validator("tone_of_voice", "style", "brand_sample", mode="before")
    @classmethod
    def optional_trim_or_none(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v or None

class CopyResponse(BaseModel):
    generated_copy: str
    keywords: List[str]
    tone_used: str
    content_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)