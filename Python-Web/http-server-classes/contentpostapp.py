#!/usr/bin/env python3

# ContentPostApp class
# Simple web application for serving content,
# admiting POST requests for accepting content
#
# Copyright Jesus M. Gonzalez-Barahona 2022
# jgb @ gsyc.es
# SARO, SAT, ST subjects (Universidad Rey Juan Carlos)

from urllib import parse

import webapp

FORM = """
    <hr>
    <form action="/" method="post" accept-charset="UTF-8">
      <div>
        <label>Resource: </label>
        <input type="text" name="resource" required>
      </div>
      <div>
        <label>Content: </label>
        <textarea name="content" rows="5" cols="33" required></textarea>
      </div>
      <div>
        <input type="submit" value="Submit">
      </div>
    </form>
"""

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
  <body>
    <div>
      <p>Content for {resource}:</p> {content}
    </div>
    <div>
      {form}
    </div>
  </body>
</html>
"""

PAGE_NOT_FOUND = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
  <body>
    <div>
      <p>Resource not found: {resource}.</p>
    </div>
    <div>
      {form}
    </div>
  </body>
</html>
"""

PAGE_NOT_ALLOWED = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
  <body>
    <p>Method not allowed: {method}.</p>
  </body>
</html>
"""

PAGE_UNPROCESABLE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
  <body>
    <p>Unprocesable POST: {body}.</p>
  </body>
</html>
"""

class ContentApp(webapp.webApp):

    def __init__(self, hostname, port):
        self.contents = {}
        super().__init__(hostname, port)

    def parse (self, request):
        """Return the method name and resource name"""

        data = {}
        body_start = request.find('\r\n\r\n')
        if body_start == -1:
            data['body'] = None
        else:
            data['body'] = request[body_start+4:]
        parts = request.split(' ', 2)
        data['method'] = parts[0]
        data['resource'] = parts[1]
        return (data)

    def process (self, data):
        """Produce the page with the content for the resource"""

        if data['method'] == 'GET':
            code, page = self.get(data['resource'])
        elif data['method'] == 'PUT':
            code, page = self.put(data['resource'], data['body'])
        elif data['method'] == 'POST':
            code, page = self.post(data['resource'], data['body'])
        else:
            code, page = "405 Method not allowed",\
                         PAGE_NOT_ALLOWED.format(method=data['method'])
        return (code, page)

    def get(self, resource):
        if resource in self.contents:
            content = self.contents[resource]
            page = PAGE.format(content=content, resource=resource, form=FORM)
            code = "200 OK"
        else:
            page = PAGE_NOT_FOUND.format(resource=resource, form=FORM)
            code = "404 Resource Not Found"
        return code, page

    def put(self, resource, body):
        self.contents[resource] = body
        page = PAGE.format(content=body, resource=resource, form=FORM)
        code = "200 OK"
        return code, page

    def post(self, resource, body):
        fields = parse.parse_qs(body, encoding='utf-8')
        print("Fields:", fields)
        if (resource == '/'):
            if ('resource' in fields) and ('content' in fields):
                resource = fields['resource'][0]
                content = fields['content'][0]
                self.contents[resource] = content
                page = PAGE.format(content=content, resource=resource, form=FORM)
                code = "200 OK"
            else:
                page = PAGE_UNPROCESABLE.format(body=body)
                code = "422 Unprocessable Entity"
        else:
            code = "405 Method not allowed"
            page = PAGE_NOT_ALLOWED.format(method='POST')
        return code, page

if __name__ == "__main__":
    webApp = ContentApp ("localhost", 1234)
