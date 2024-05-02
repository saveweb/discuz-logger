# from rich import print
import httpx
from tqdm import tqdm

from discuz_logger.define.check import ResponseCheck
from discuz_logger.define.forum_index import ResponseForumIndex
from discuz_logger.utils import APIHelper
# https://bbs.emath.ac.cn/api/mobile/index.php?check=check


class MobileApi:
    client: httpx.AsyncClient
    base_url: str
    API_PATH: str = "/api/mobile/index.php"

    def __init__(self, client: httpx.AsyncClient, site: str):
        self.client = client
        assert not site.endswith("/")
        self.base_url = site

    async def check_mobile_api(self):
        r = await self.client.get(
            self.base_url + "/api/mobile/index.php", params={"check": "check"}
        )
        return ResponseCheck(**r.json()), r

    @property
    def bbs_logo_url(self):
        return self.base_url + "/static/image/common/logo.png"

    def get_bbs_medal_image_url(self, image):
        return self.base_url + f"/static/image/common/{image}"

    def get_bbs_mobile_image_url(self, image):
        return self.base_url + f"/static/image/mobile/{image}"

    @property
    def login_web_url(self):
        return self.base_url + "/member.php?mod=logging&action=login"

    def get_attachment_with_alien_code(self, alien_code):
        return self.base_url + "/forum.php?mod=attachment&aid=" + alien_code

    async def get_forum_index(self):
        r = await self.client.get(
            self.base_url + self.API_PATH, params={"version": 4, "module": "forumindex"}
        )
        index = ResponseForumIndex(**r.json())
        return index, r

    async def viewthread(self, tid, page=1):
        r = await self.client.get(
            self.base_url + self.API_PATH,
            params={"version": 4, "module": "viewthread", "tid": tid, "page": page},
        )
        return r.json(), r

    # p?mod=forumdisplay&fid=2&orderby=dateline&orderby=dateline&filter=author&page=4&t=1812754
    async def forumdisplay(self, fid, page=1, orderby="dateline", filter="author"):
        r = await self.client.get(
            self.base_url + self.API_PATH,
            params={
                "version": 4,
                "module": "forumdisplay",
                "fid": fid,
                "page": page,
                "orderby": orderby,
                "filter": filter,
            },
        )
        return r.json()

    # forum.php?mod=forumdisplay&fid=39
    # forum.php?mod=forumdisplay&fid=39&orderby=dateline&filter=author&orderby=dateline&page=2
    # forum.php?mod=redirect&tid=479118&goto=lastpost # lastpost 跳转到最后一页最后一个回复
    async def iter_threads(self, fid: str | int):
        page = 1
        forumdisplay = await self.forumdisplay(fid, page=page)
        assert int(forumdisplay["Variables"]["forum"]["threads"]) <= int(
            forumdisplay["Variables"]["forum"]["threadcount"]
        )
        threads_total: int = int(forumdisplay["Variables"]["forum"]["threads"])
        threads_fetched: int = 0
        tqd = tqdm(total=threads_total, desc=f"fid={fid}", unit="threads",dynamic_ncols=True)
        while threads_fetched < threads_total:
            forumdisplay = await self.forumdisplay(fid, page=page)
            threads_total = int(forumdisplay["Variables"]["forum"]["threads"])
            threads = APIHelper.get_thread_metas(forumdisplay)
            for thread in threads:
                yield thread

            threads_fetched += len(threads)
            page += 1

            tqd.total = threads_total
            tqd.update(len(threads))
        tqd.close()
