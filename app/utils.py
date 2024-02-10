from typing import Generic, TypeVar, Optional, Union, List
from pydantic import BaseModel
# Define a generic type variable
T = TypeVar("T")


# Define a response wrapper to construct GenericResponse
def response_wrapper(status: str, message: str,  data=None,  error=None):
    return {"status": status, "message": message, "data": data, "error": error}


# Generic response model to send responses in a standard format
class GenericResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Union[List[T], T, None]
    error: Optional[dict]
