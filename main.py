from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl
import random
import string


def make_short_url() -> str:
	uniqueValues = string.ascii_letters + string.digits
	return ''.join(random.choices(uniqueValues, k=6))

linkDict = {}

app = FastAPI()

@app.get("/")
async def read_root():
	return "Home page!"

@app.post("/shorturl")
def shorten_url(url: HttpUrl):
	shortURL = make_short_url()
	linkDict[shortURL] = url.url
	return {"short_url": shortURL}

@app.get("/shorturl/{shortURL}")
def read_url(shortURL: str):
	if shortURL not in linkDict.keys():
		raise HTTPException(status_code=404, detail="URL not found")
	return linkDict[shortURL]
