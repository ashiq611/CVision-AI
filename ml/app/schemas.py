from typing import List, Optional, Dict, Union
from pydantic import BaseModel

class Education(BaseModel):
    degree: Optional[str]
    institution: Optional[str]
    start_year: Optional[Union[str, int, None]]
    end_year: Optional[Union[str, int, None]]

class Work(BaseModel):
    title: Optional[str]
    company: Optional[str]
    start: Optional[str]
    end: Optional[str]
    description: Optional[str]

class CVResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    summary: Optional[str]
    education: List[Education]
    work_experience: List[Work]
    skills: List[str]
    certifications: List[str]
    languages: List[str]
    address: Optional[str]
    other: Dict
