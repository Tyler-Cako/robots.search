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

            #print(f"Papers found: {self.papers.keys()}")

            #print("Storing HTML into a csv...")
            return writePagesToCSV(self.papers)

    async def crawlUrl(self, url: str, counter: int) -> None:
        if url in self.visited:
            return
        self.visited.add(url)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                self.visited.add(url)
                print(f"crawlUrl: {url} counter: {counter}")
                response = await client.get(url)
                responseHtml = response.text

                #response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                #print(f"URL: {url} | Status: {response.status_code} | Final URL: {str(response.url)}")

                if response.history:
                    print(f"Redirect history for {url}:")
                    for r in response.history:
                        print(f"{r.status_code} → {r.headers.get('location')}")

                htmlParser = HTMLParser()
                isPaper, url_list, error_list = htmlParser.run(url, responseHtml)

                self.error_list.extend(error_list)

                if isPaper:
                    #print(f"paper: {url}")
                    #print(f"Length of HTML: {len(responseHtml)}")
                    self.papers[url] = responseHtml
                
                if counter <= 0:
                    return

                tasks = []
                for url in url_list:
                    if self.hostname in getHostName(url):
                        tasks.append(asyncio.create_task(self.crawlUrl(url, counter - 1)))
                
                await asyncio.gather(*tasks)
            except :
                print("error loading page")
                self.error_list.extend(url)
                return