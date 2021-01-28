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

# Deployment

`uwsgi.py` is production-ready, just change `/path/to/httpecho` to your real path and create `/var/log/httpecho` and
make sure that your server's user (usually `www-data`) has `rw` rights to it.

Example NginX config (all HTTP traffic redirected to HTTPS):

```nginx
server {
    listen 80;
    server_name echo.example.com;
    server_tokens off;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name echo.example.com;
    server_tokens off;

    ssl_session_cache shared:le_nginx_SSL:10m;
    ssl_session_timeout 1440m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";
    ssl_certificate /etc/letsencrypt/live/echo.example.com/fullchain.pem;
    ssl_certificate_key	/etc/letsencrypt/live/echo.example.com/privkey.pem;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/path/to/httpecho/uwsgi.sock;
        uwsgi_read_timeout 20;
    }
}
```

# Credits

- CSS of the index page is from this great tiny article:
  [58 bytes of css to look great nearly everywhere](https://jrl.ninja/etc/1/).
