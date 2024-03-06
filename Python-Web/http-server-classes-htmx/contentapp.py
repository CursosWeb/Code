#!/usr/bin/env python3

# ContentApp class (HTMX version)
# Simple web application for serving content,
# with an API admitting GET (for getting documents)
# and PUT (for updating documents)
#
# Copyright Jesus M. Gonzalez-Barahona 2024
# jesus.gonzalez.barahona @ urjc.es
# SARO, SAT, ST subjects (Universidad Rey Juan Carlos)

import webapp

ROOT = """
<!DOCTYPE html>
<html lang='en'>
  <head>
    <script src='https://unpkg.com/htmx.org@1.9.10'></script>
  </head>
  <body>
    <button hx-get='/hola'
      hx-trigger='click'
      hx-target='#content'
      hx-swap='outerHTML'>
      Click Me
    </button>
    <div id='content'></div>
  </body>
</html>
"""

PAGE_NOT_FOUND = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Resource not found: {resource}.</p>
  </body>
</html>
"""

PAGE_NOT_ALLOWED = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Method not allowed: {method}.</p>
  </body>
</html>
"""

class ContentApp(webapp.WebApp):

    def __init__(self, hostname, port):
        self.contents = {"/": ROOT, "/hola": "Hola"}
        super().__init__(hostname, port)

    def parse (self, request):
        """Return the method name and resource name"""

        data = {}
        body_start = request.find('\r\n\r\n')
        if body_start == -1:
            data['body'] = None
        else:
            data['body'] = request[body_start:]
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
        else:
            code, page = "405 Method not allowed",\
                         PAGE_NOT_ALLOWED.format(method=data['method'])
        return (code, page)

    def get(self, resource):
        if resource in self.contents:
            page = self.contents[resource]
            code = "200 OK"
        else:
            page = PAGE_NOT_FOUND.format(resource=resource)
            code = "404 Resource Not Found"
        return code, page

    def put(self, resource, body):
        self.contents[resource] = body
        page = PAGE.format(content=body)
        code = "200 OK"
        return code, page

if __name__ == "__main__":
    webApp = ContentApp ("localhost", 1234)
