
from dataclasses import dataclass
from typing import Optional


@dataclass
class Post:
    pid: str
    tid: str
    first: str
    author: str
    authorid: str
    dateline: str
    message: str
    anonymous: str
    attachment: str
    status: str
    replycredit: str
    position: str
    groupid: str
    dbdateline: str
    groupiconid: str

    adminid: Optional[str] = None
    attachments: Optional[list] = None
    imagelist: Optional[list] = None
    memberstatus: Optional[str] = None
    username: Optional[str] = None
    attachlist: Optional[list] = None
    number: Optional[str] = None
