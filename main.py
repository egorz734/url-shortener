from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import random
import string


class URL(BaseModel):
	url: str

def make_short_url() -> str:
	uniqueValues = string.ascii_letters + string.digits
	return ''.join(random.choices(uniqueValues, k=6))

conn = sqlite3.connect('data/db.sqlite')
try:
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE urltable (shorturl VARCHAR(64) not null,'
				'longurl VARCHAR(64) not null)')
	conn.commit()
except:
	print('DB already exist!')

app = FastAPI()

@app.get("/")
async def read_root():
	return "Home page!"

@app.post("/shorturl")
def shorten_url(url: URL):
	conn = sqlite3.connect('data/db.sqlite')
	shortURL = make_short_url()
	cursor = conn.cursor()
	cursor.execute(f'INSERT INTO urltable (shorturl, longurl) VALUES (\'{shortURL}\', \'{url.url}\')')
	conn.commit()
	return {"short_url": shortURL}

@app.get("/shorturl/{shortURL}")
def read_url(shortURL: str):
	conn = sqlite3.connect('data/db.sqlite')
	cursor = conn.cursor()
	cursor.execute(f'SELECT * FROM urltable WHERE shorturl=\'{shortURL}\'')
	resultList = cursor.fetchall()
	if len(resultList) == 0:
		raise HTTPException(status_code=404, detail="URL not found")
	elif len(resultList) != 1:
		raise HTTPException(status_code=404, detail="Multiple URLs were found")
	return resultList
