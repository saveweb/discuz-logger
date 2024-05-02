import asyncio
import json
from pathlib import Path
from typing import Coroutine, Tuple

import httpx
from tqdm import tqdm

from discuz_logger.define.forum_index import Forumlist
from discuz_logger.define.thread import ThreadMeta
from discuz_logger.mobile_api import MobileApi
from discuz_logger.utils import APIHelper, arg_parser, json_dump

async def forum_worker(queue: asyncio.Queue[Coroutine]):
    while True:
        task = await queue.get()
        await task
        queue.task_done()


async def thread_worker(queue: asyncio.Queue[Tuple[MobileApi, ThreadMeta, Path]]):
    no_first_check = True
    while True:
        site, thread_meta, thread_dir = await queue.get()
        thread_dir.mkdir(parents=True, exist_ok=True)

        maxposition = maxposition_last_run = -1
        fetched_postion = -2
        thread_json_path = thread_dir / "thread.json"
        if thread_json_path.exists():
            if no_first_check:
                continue
            thread = json.loads(thread_json_path.read_text())
            maxposition_last_run = int(thread["maxposition"])
        viewthread = None
        tqd = None
        page = 1
        while fetched_postion < maxposition:
            for t in range(3):
                try:
                    viewthread, _ = await site.viewthread(thread_meta.tid, page=page)
                except Exception as e:
                    if t == 2:
                        raise e
                    print(f"tid={thread_meta.tid} page={page} ,retry={t} error:{e}")
                    await asyncio.sleep(10)
                    continue
            maxposition = APIHelper.get_maxposition(viewthread)

            if maxposition == maxposition_last_run:
                break
            if len(APIHelper.get_posts(viewthread)) == 0:
                assert int(thread_meta.readperm) != 0
                print(f"tid={thread_meta.tid} readperm:{thread_meta.readperm}")
                break

            if tqd is None:
                tqd = tqdm(desc=f"tid={thread_meta.tid} subj:{thread_meta.subject}", unit="posts", dynamic_ncols=True)

            for post, post_raw in APIHelper.get_posts(viewthread):
                fetched_postion = int(post.position) if int(post.position) > fetched_postion else fetched_postion

                with open(thread_dir / f"pid-{post.pid}.json", "w") as f:
                    f.write(json_dump(post_raw))

            if fetched_postion < 0:
                fetched_postion = 0

            tqd.total = maxposition
            tqd.n = fetched_postion
            tqd.refresh()

            page += 1

        assert viewthread is not None
        thread_json_path.write_text(json_dump(APIHelper.get_thread(viewthread)))

        tqd.close() if tqd is not None else None
        queue.task_done()


async def _main():
    args = arg_parser()

    forum_queue: asyncio.Queue[Coroutine] = asyncio.Queue(maxsize=5)
    threads_queue: asyncio.Queue[Tuple[MobileApi, ThreadMeta, Path]] = asyncio.Queue(maxsize=100)
    for i in range(5):
        asyncio.create_task(forum_worker(forum_queue))
    for i in range(3):
        asyncio.create_task(thread_worker(threads_queue))

    transport = httpx.AsyncHTTPTransport(retries=5, http1=True, http2=True)
    client = httpx.AsyncClient(transport=transport, headers={"User-Agent": "saveweb/0.1 (bbs@saveweb.org)"}, timeout=30)
    site = MobileApi(client, args.site)
    check, r = await site.check_mobile_api()
    site_dir = Path("data") / "site" / check.mysiteid
    site_dir.mkdir(parents=True, exist_ok=True)
    with open(site_dir / "check.json", "w") as f:
        f.write(json_dump(r.json()))
    print(check)
    index, _ = await site.get_forum_index()

    async def put_threads_to_queue(forum: Forumlist):
        async for thread in site.iter_threads(forum.fid):
            await threads_queue.put((site, thread, site_dir / "thread" / thread.tid))

    for forum in index.forumlist:
        co = put_threads_to_queue(forum)
        await forum_queue.put(co)

    await forum_queue.join()
    await threads_queue.join()


def main():
    asyncio.run(_main())

if __name__ == "__main__":
    main()