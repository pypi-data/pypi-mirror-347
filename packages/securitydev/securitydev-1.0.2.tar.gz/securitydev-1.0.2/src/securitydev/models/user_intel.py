from typing import List

from pydantic import BaseModel


class EmailIntelResponse(BaseModel):
    """Response model for the email intelligence endpoint."""
    valid: bool
    disposable: bool
    providers: List[str]
