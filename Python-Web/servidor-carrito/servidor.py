#!/usr/bin/env python3
"""
Servidor HTTP sencillo que responde a peticiones GET con un mensaje básico.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import random

last_usu = 0

carrito = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Manejador simple de peticiones HTTP."""
    
    def do_GET(self):
        """Maneja peticiones GET."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Servidor HTTP Sencillo</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>SuperServidorWeb</h1>
            <h2>¡Hola desde el servidor HTTP!</h2>
            <p>Este es un servidor HTTP muy básico escrito en Python.</p>
            <p>Recurso solicitado: {recurso}</p>
            <p>Usuario: {usu}</p>
            <p><a href="/{enlace}/{usu}">Enlace</a></p>
            <form method="POST" action="/carrito">
                <input type="hidden" name="usu" value="{usu}">
                <input type="hidden" name="object" value="{object}">
                <button type="submit">Añade al carrito</button>
            </form>
        </body>
        </html>
        """

        componentes = self.path.split("/")
        global last_usu
        if (len(componentes) > 2) and (componentes[2] != ""):
            usu = componentes[2]
        else:
            usu = last_usu
            last_usu += 1
        object = str(random.randint(0, 100000))
        enlace = "enlace" + object
        html_content = html_template.format(recurso=self.path, usu=usu, object=object, enlace=enlace)
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        """Maneja peticiones POST."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Leer datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        grupos = post_data.split("&")
        for grupo in grupos:
            nombre, valor = grupo.split("=")
            if nombre == "usu":
                usu = valor
            elif nombre == "object":
                object = valor
        carrito[usu] = object

        response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Servidor HTTP Sencillo</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>SuperServidorWeb</h1>
            <h2>Carrito</h2>
            <p>Usuario y objecto añadidos al carrito: {usu}, {object}</p>
            <p>Carrito: {carrito}</p>
            <p><a href="/">Volver al inicio</a></p>
        </body>
        </html>
        """
        
        self.wfile.write(response.encode('utf-8'))

def run_server(port=8000):
    """Inicia el servidor HTTP en el puerto especificado."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"Servidor iniciado en http://localhost:{port}")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
