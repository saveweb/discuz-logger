from dataclasses import dataclass

# {
# "tid": "23816",
# "typeid": "9",
# "readperm": "0",
# "price": "0",
# "author": "gl695133087",
# "authorid": "54639",
# "subject": "关于一些homeassistant启动后掉线的经验",
# "dateline": "2023-12-31",
# "lastpost": "2023-12-31 11:15",
# "lastposter": "gl695133087",
# "views": "570",
# "replies": "0",
# "displayorder": "0",
# "digest": "0",
# "special": "0",
# "attachment": "0",
# "recommend_add": "0",
# "replycredit": "0",
# "dbdateline": "1703992521",
# "dblastpost": "1703992521",
# "rushreply": "0",
# "reply": [
#     {
#     "pid": "581729",
#     "author": "pangls",
#     "authorid": "82180",
#     "message": "百度胖老师吧上海宝山公安通河新村派出所民警欺负绑 架谋杀胖老师百度360搜索百度胖老师吧上海宝山公安通河 ..."
#     }
# ]
# },
@dataclass
class ThreadMeta:
    tid: str
    typeid: str
    readperm: str
    price: str
    author: str
    authorid: str
    subject: str
    dateline: str
    lastpost: str
    lastposter: str
    views: str
    replies: str
    displayorder: str
    digest: str
    special: str
    attachment: str
    recommend_add: str
    replycredit: str
    dbdateline: str
    dblastpost: str
    rushreply: str
    reply: list

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"<ThreadMeta {' '.join([f'{k}={v}' for k, v in self.__dict__.items()])}>"
