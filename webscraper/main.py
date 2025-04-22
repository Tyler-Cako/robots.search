from crawler.Crawler import Crawler
import asyncio

crawler = Crawler()

async def main():
    print("running Crawler...")
    if not (await crawler.run("url_list.txt", 1)):
        print("Web crawl failed!")
        return
    
    print("Web crawl successful")
    #print(f"Papers found: {papers.keys()}")

    # print("Storing HTML into a csv...")
    


asyncio.run(main())
