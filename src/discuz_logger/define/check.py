from dataclasses import dataclass

@dataclass
class ResponseCheck:
    discuzversion: str
    """ X3.4 """
    charset: str
    """ utf-8"""
    version: str
    """ 4 """
    pluginversion: str
    """ 1.4.7 """
    oemversion: str
    """ 0 """
    regname: str
    """ ref """
    qqconnect: str
    """ 0 """
    sitename: str
    """ 论坛名 """
    mysiteid: str
    """ 论坛id? """
    ucenterurl: str
    """ https://avatar.elecfans.com/uc_server """
    setting: dict
    """ {'closeforumorderby': '0'} """
    extends: dict
    """ {'used': None, 'lastupdate': None}) """