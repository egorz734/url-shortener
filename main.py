from fastapi import FastAPI
import random
import string
from pydantic import BaseModel


class URL(BaseModel):
	url: str

def make_short_url() -> str:
	uniqueValues = string.ascii_letters + string.digits
	return ''.join(random.choices(uniqueValues, k=6))

linkDict = {}

app = FastAPI()

@app.get("/")
async def read_root():
	return "Home page!"

@app.post("/shorturl")
def shorten_url(url: URL):
	shortURL = make_short_url()
	linkDict[shortURL] = url.url
	return {"short_link": shortURL}

@app.get("/shorturl/{shortURL}")
def read_url(shortURL: str):
	if shortURL not in linkDict.keys():
		'''return 404'''
		print(linkDict)
		pass
	return linkDict[shortURL]
