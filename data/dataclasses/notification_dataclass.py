from dataclasses import dataclass


@dataclass
class Notification:
    user_id: int
    message: str
    sent_at: str
    read: bool = False
