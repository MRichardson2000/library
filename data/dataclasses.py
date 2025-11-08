from dataclasses import dataclass


@dataclass(frozen=True)
class DB:
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
