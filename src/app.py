import datetime
import time
from http import HTTPStatus
from typing import Union, Dict

from flask import Flask, Response, request, make_response, render_template


app = Flask(__name__)


def _str_removesuffix(str_, suffix: str):
    if len(suffix) > 0 and str_.endswith(suffix):
        return str_[: -len(suffix)]
    else:
        return str_


def _build_body(status_code, talk_json):
    body: Union[Dict[str, Union[str, int]], str]

    try:
        status = HTTPStatus(status_code)
    except ValueError:
        if talk_json:
            body = {"code": status_code, "description": "Unkown"}
        else:
            body = f"{status_code} Unknown"
    else:
        if talk_json:
            body = {"code": status.value, "description": status.phrase}
        else:
            body = f"{status.value} {status.phrase}"

    return body


def _parse_sleep_duration() -> int:
    sleep_duration = request.args.get("sleep", 0)
    try:
        sleep_duration = int(sleep_duration)
    except (TypeError, ValueError):
        sleep_duration = 0
    else:
        # Max sleep = 5 minutes
        sleep_duration = min(sleep_duration, 300000)
    return sleep_duration


@app.route("/<int:status_code>")
def echo(status_code: int) -> Response:
    # Content type
    if request.accept_mimetypes.accept_json:
        talk_json = True
    else:
        talk_json = False

    # Headers
    headers = {
        "Content-Type": "application/json; charset=utf8" if talk_json else "text/plain; charset=utf8",
        "Cache-Control": "max-age=0, no-cache, no-store, must-revalidate, private",
        "Expires": datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "Content-Security-Policy": "script-src 'self' 'unsafe-inline' blob:; img-src 'self' data:; style-src 'self' "
        "'unsafe-inline'; font-src 'self'; base-uri 'self'; connect-src 'self'; form-action 'self'; default-src 'none'",
        "X-Frame-Options": "DENY",
        "Vary": "Accept-Language, Cookie, Origin",
        "Content-Language": "en",
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "same-origin",
        "Access-Control-Allow-Origin": "*",
    }

    # Body
    body = _build_body(status_code, talk_json)

    # Sleep
    sleep_duration = _parse_sleep_duration()
    headers["X-Sleep"] = str(sleep_duration)
    time.sleep(sleep_duration / 1000)
    response = make_response(body, status_code, headers)

    return response


@app.route("/")
def index():
    context = {"base_url_without_path": _str_removesuffix(request.base_url, request.path)}
    return render_template("index.html", **context)


@app.route("/robots.txt")
def robots():
    return make_response(render_template("robots.txt"), {"Content-Type": "text/plain; charset=utf8"})


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
