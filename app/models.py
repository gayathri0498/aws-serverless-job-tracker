from pydantic import BaseModel, Field
from typing import Optional, Literal


class JobApplication(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)

    status: Literal[
        "Applied",
        "Screening",
        "Interview",
        "Offer",
        "Rejected",
        "Withdrawn"
    ]

    location: Optional[str] = Field(default=None, max_length=100)
    date_applied: Optional[str] = None