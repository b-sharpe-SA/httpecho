# HttpEcho

HttpEcho is a dead simple echo app that responds to a request with the desired HTTP status code. It is heavily inspired
by [httpstat.us](https://httpstat.us).

## Features

- Handles known and unknown HTTP statuses.
- Set optional custom delay between request and response (useful to test-trigger timeouts).
- CORS-ready.
- FOSS.

## Example requests and responses:

- Simplest 200:
```
==> curl http://127.0.0.1:5000/200
<== {"code": 200, "description": "OK"}
```

- 200 with 2500ms delay:
```
==> curl http://127.0.0.1:5000/200?sleep=2500
🕜 wait approximately 2.5s
<== {"code": 200, "description": "OK"}
```

- 404:
```
==> curl http://127.0.0.1:5000/404
<== {"code": 404, "description": "Not Found"
```

- 666 (custom status):
```
==> curl http://127.0.0.1:5000/666
<== {"code": 666, "description": "Unknown"}
```

# Details

- Response will be encoded in JSON whenever possible, just make sure your `Accept` request header allows it.
- Max sleep duration is 5 minutes (could be less depending on your server configuration).

# Credits

- CSS of the index page is from this great tiny article:
  [58 bytes of css to look great nearly everywhere](https://jrl.ninja/etc/1/).
