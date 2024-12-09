from fastapi import FastAPI
from src.Scrapping.CrawlScrapper import CrawlScrapper
from src.Scrapping.DinamicScrapper import HandlerDinamic

app = FastAPI(title="API de CrawlScrapper")


@app.get("/scrape")
async def scrape_dynamic(url: str):
    result = await run_scraper(url)
    return {"result": result}

@app.get("/generate-markdown")
async def generate_markdown(url: str):
    result = await generate_markdown_content(url)
    return {"result": result}

async def run_scraper(url):
    result = HandlerDinamic(url)
    return result

async def generate_markdown_content(url):
    result = await CrawlScrapper(url)
    return result
