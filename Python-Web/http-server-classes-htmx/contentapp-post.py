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

PAGE = """
<!DOCTYPE html>
<html lang='en'>
  <head>
    <script src='https://unpkg.com/htmx.org@1.9.10'></script>
  </head>
  <body>
    <div>
        <div>
            Current content: <div id=content></div>
        </div>
        <button hx-get='/content/{resource}'
          hx-trigger='click'
          hx-target='#content'
          hx-swap='innerHTML'>
          Get
        </button>
    </div>
    <div>
        <div>
            New content: <input name='content' type='text'/>
        </div>
        <button hx-post='/content/{resource}'
          hx-include="[name='content']"
          hx-trigger='click'
          hx-target='#content'
          hx-swap='innerHTML'>
          Post
        </button>
    </div>
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
        self.contents = {}
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
        elif data['method'] == 'POST':
            code, page = self.post(data['resource'], data['body'])
        else:
            code, page = "405 Method not allowed",\
                         PAGE_NOT_ALLOWED.format(method=data['method'])
        return (code, page)

    def get(self, resource):
        print("RESOURCE:", resource)
        if resource.startswith('/content/'):
            content_res = resource.split('/', 3)[2]
            if content_res in self.contents:
                page = self.contents[content_res]
                code = "200 OK"
            else:
                page = PAGE_NOT_FOUND.format(resource=resource)
                code = "404 Resource Not Found"
        else:
            page = PAGE.format(resource=resource[1:])
            code = "200 OK"
        return code, page

    def post(self, resource, body):
        if resource.startswith('/content/'):
            content_res = resource.split('/', 3)[2]
            qs_elems = body.split('=')
            content = qs_elems[1]
            self.contents[content_res] = content
            page = content
            code = "200 OK"
        elif resource in self.contents:
            code, page = "405 Method not allowed", \
                PAGE_NOT_ALLOWED.format(method='POST')
        else:
            page = PAGE_NOT_FOUND.format(resource=resource)
            code = "404 Resource Not Found"
        return code, page

if __name__ == "__main__":
    webApp = ContentApp ("localhost", 1234)
