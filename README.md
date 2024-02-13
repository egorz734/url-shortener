# URL-shortener

creates a shortcut for URL

# future plans:
## db
- [x] Add mysql db to store urls
  - [x] Make db interaction with raw SQL (https://github.com/egorz734/url-shortener/tree/sqlite-v0.1)
  - [x] Add ORM with `sqlalchemy` (https://github.com/egorz734/url-shortener/tree/sqlite-v0.2)
- [ ] Move to postgresql (for exmaple) which is run as a separate service
- [ ] Try adding expiration time for shortcuts
## docker
- [ ] create docker-compose for the project
## analytics
- [ ] collect number of time link is used
- [ ] collect time it takes to "unfold" the shortcut link
- [ ] add logging

# example usage
`curl -X POST -d '{"url": "https://google.com"}' -H "Content-Type: application/json" http://localhost:8000/shorturl`
