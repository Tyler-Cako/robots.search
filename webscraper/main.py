from crawler.Crawler import Crawler
import asyncio

crawler = Crawler()

async def main():
    print("running Crawler...")
    if not (await crawler.run("url_list.txt", 12)):
        print("Web crawl failed!")
        return
    
    print("Web crawl successful")
    


asyncio.run(main())
