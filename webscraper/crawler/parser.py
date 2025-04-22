from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import urlopen
from typing import List, Tuple, Generator
from .util import cleanUrl, getHostName, isValid, isPaper
import re

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]):
        """Handle <a> tags to continue crawling"""
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    new_url = urljoin(self.url, value) #Make relative url absolute
                    formatted_url = cleanUrl(new_url)

                    if isValid(formatted_url, self.hostname):
                        print(f"valid url: {formatted_url}, {self.hostname}")
                        self.url_list.append(formatted_url)

    def run(self, url, html: str) -> Tuple[bool, List[str], List[str]]:
        """Parse a given URL's page. Returns list of links to crawl next"""

        self.hostname = getHostName(url)
        self.url = url
        self.url_list = []
        self.error_list = []
        self.is_paper = False

        try:
            self.feed(html)

            if isPaper(url):
                self.is_paper = True 

        except Exception as e:
            print(f"Parsing error from url({url}): {e}")
            self.error_list.append(url)

        return self.is_paper, self.url_list, self.error_list