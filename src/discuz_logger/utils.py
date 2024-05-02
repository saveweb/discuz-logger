import argparse
from dataclasses import dataclass
import json

from discuz_logger.define.post import Post
from discuz_logger.define.thread import ThreadMeta

@dataclass
class Args:
    site: str

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=str, required=True)
    return Args(**vars(parser.parse_args()))


class APIHelper:
    @staticmethod
    def get_thread_metas(forumdisplay):
        return [
            ThreadMeta(**thread)
            for thread in forumdisplay["Variables"]["forum_threadlist"]
        ]
    @staticmethod
    def get_maxposition(viewthread)->int:
        return int(viewthread["Variables"]["thread"]["maxposition"])
    @staticmethod
    def get_posts(viewthread):
        return [(Post(**post), post)
                for post in viewthread["Variables"]["postlist"]]
    @staticmethod
    def get_thread(viewthread):
        return viewthread["Variables"]["thread"]

def json_dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))