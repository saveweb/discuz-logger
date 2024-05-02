from dataclasses import dataclass

@dataclass
class Catlist:
    fid: str
    name: str
    forums: str


class Forumlist:
    fid: str
    name: str
    threads: str
    """ 不准确 """
    posts: str
    """ 不准确 """
    todayposts: str
    description: str
    icon: str
    sublist: list

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def __repr__(self):
        return f"<Forumlist {' '.join([f'{k}={v}' for k, v in self.__dict__.items()])}>"

@dataclass
class ResponseForumIndex:
    Version: str
    """ 4 """
    Charset: str
    """ UTF-8 """
    Variables: dict

    @property
    def catlist(self):
        return [Catlist(**cat) for cat in self.Variables["catlist"]]
    
    @property
    def forumlist(self):
        return [Forumlist(**forum) for forum in self.Variables["forumlist"]]