import asyncio

import httpx
from .parser import HTMLParser
from .util import getHostName, writePagesToCSV

from typing import Dict


class Crawler(object):
    def __init__(self):
        self.papers = {} # Dict of papers found when crawling schema: <url>:<html>
        self.visited = set([]) # Set of visited URLs for traversal
        self.error_list = [] # List of URLs that were not parse-able
        self.htmlParser = HTMLParser()
        self.hostname = ""

    async def run(self, path: str, depth: int) -> Dict[str, str]:
        """Start URL crawling given file path to a list of urls"""

        with open(path) as file:

            url = file.readline()
            self.hostname = getHostName(url)
            # Read list of files from txt document

            tasks = []
            while url:
                print(f"url: {url}")
                tasks.append(asyncio.create_task(self.crawlUrl(url.rstrip(), depth)))
                url = file.readline()
            
            await asyncio.gather(*tasks)

            print(f"Papers found: {self.papers.keys()}")

            print("Storing HTML into a csv...")
            return writePagesToCSV(self.papers)

    async def crawlUrl(self, url: str, counter: int) -> None:
        if url in self.visited:
            return
        self.visited.add(url)

        async with httpx.AsyncClient() as client:
            self.visited.add(url)
            print(f"crawlUrl: {url} counter: {counter}")
            response = await client.get(url)
            responseHtml = response.text
            isPaper, url_list, error_list = self.htmlParser.run(url, responseHtml)

            self.error_list.extend(error_list)

            if isPaper:
                self.papers[url] = responseHtml
            
            if counter <= 0:
                return

            tasks = []
            for url in url_list:
                if self.hostname in getHostName(url):
                    tasks.append(asyncio.create_task(self.crawlUrl(url, counter - 1)))
            
            await asyncio.gather(*tasks)
