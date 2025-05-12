```
usage: web-session-retriever [-h] [--cookie COOKIE] [--on-redirect ON_REDIRECT] url

Browse a URL using botasaurus

positional arguments:
  url                        URL to visit

options:
  --cookie COOKIE            Return only this cookie
  --on-redirect ON_REDIRECT  Terminate when redirected to this URL
```

```sh
web-session-retriever https://www.example.com/login --on-redirect https://www.example.com/home

or

web-session-retriever https://www.example.com/login
```
