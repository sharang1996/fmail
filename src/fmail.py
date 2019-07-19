#!/usr/bin/env python3
"""FMail web page and API."""

from falcon import API, HTTP_200, HTTP_500
from tasks.send_email import sendmail
import sys


class SendEmail:
    """FMail API."""
    def on_post(self, req, resp):
        """POST handler for FMail API endpoint."""
        promise = sendmail.delay(req.media['to_addr'], req.media['subject'],
                                 req.media['body'], req.media['from_addr'], req.media['password'])
        resp.status = HTTP_200 if promise else HTTP_500

    def on_get(self, req, resp):
        """GET handler for FMail Webpage."""
        resp.content_type = 'text/html'
        resp.body = """\
<!DOCTYPE html>
<html>
    <head>
        <title>FMail</title>
        <script>
            function submit() {
                var to_addr = document.getElementById("to_addr").value;
                var subject = document.getElementById("subject").value;
                var body = document.getElementById("body").value;
                var password = document.getElementById("password").value;
                var from_addr = document.getElementById("from_addr").value;

                var postdata = JSON.stringify({
                    "to_addr": to_addr,
                    "subject": subject,
                    "body": body,
                    "password":password,
                    "from_addr":from_addr
                });

                var xhr = new XMLHttpRequest();

                xhr.onreadystatechange = function () {
                    if (this.readyState === 4 && this.status === 200) {
                        document.getElementById("status").innerHTML = "Success.";
                    }
                    else {
                        document.getElementById("status").innerHTML = "Failure.";
                    }
                }

                xhr.open("POST", "/", true);
                xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                xhr.send(postdata);
            }
        </script>
    </head>
    <body>
    	<input id="from_addr" placeholder="From Address" type="email" />
        <br />
        <input id="to_addr" placeholder="To Address" type="email" />
        <br />
        <input id="subject" placeholder="Subject" />
        <br />
        <input id="password" placeholder="Password" type="password" />
        <br />
        <textarea id="body" width="100" height="100">
            Body
        </textarea>
        <br />
        <button type="button" onclick="submit()">
            Submit
        </button>
        <p id="status"></p>
    </body>
</html>
        """


APP = API()
APP.add_route('/', SendEmail())
