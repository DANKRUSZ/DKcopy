from typing import Literal, TypedDict, List

Role = Literal["system", "user", "assistant"]

class Message(TypedDict):
    role: Role
    content: str

Messages = List[Message]
