#!/usr/bin/env python3

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import plantillas

# Estado: diccionario para almacenar la lista de la compra
compra = {}

class CompraHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.strip('/')
        
        if path == '':
            # GET / - Página principal con la lista de elementos
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Generar lista de elementos
            if compra:
                items_html = ""
                for nombre, cantidad in sorted(compra.items()):
                    items_html += plantillas.ITEM_FORMATO.format(
                        nombre=nombre
                    )
                lista_html = plantillas.ITEM_LISTA_CON_ELEMENTOS.format(items=items_html)
            else:
                lista_html = plantillas.ITEM_LISTA_VACIA
            
            content = plantillas.PAGINA_PRINCIPAL.format(lista_items=lista_html)
            page = plantillas.HTML_BASE.format(content=content)
            
            self.wfile.write(page.encode('utf-8'))
            
        else:
            # GET /<elemento> - Página de un elemento específico
            elemento = path
            cantidad = compra.get(elemento, 0)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            content = plantillas.PAGINA_ELEMENTO.format(
                nombre=elemento,
                cantidad=cantidad
            )
            page = plantillas.HTML_BASE.format(content=content)
            
            self.wfile.write(page.encode('utf-8'))
    
    def do_POST(self):
        # Leer el cuerpo de la petición
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parsear los parámetros del formulario
        query_params = parse_qs(post_data)
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path.strip('/')
        
        if path == '':
            # POST / - Crear nuevo elemento
            if 'nombre' in query_params:
                nombre = query_params['nombre'][0].strip()
                if nombre:  # Solo añadir si el nombre no está vacío
                    if nombre not in compra:
                        compra[nombre] = 0  # Nueva cantidad es 0 por defecto
            print(compra)
            # Redirigir a GET / (mostrar la página principal)
            self.do_GET()
            
        else:
            # POST /<elemento> - Actualizar cantidad de un elemento
            elemento = path
            if 'valor' in query_params:
                try:
                    nueva_cantidad = int(query_params['valor'][0])
                    if nueva_cantidad >= 0:
                        compra[elemento] = nueva_cantidad
                except ValueError:
                    pass  # Ignorar valores no válidos
            
            # Redirigir a GET /<elemento> (mostrar la página del elemento)
            self.do_GET()
    
    def log_message(self, format, *args):
        # Sobreescribir para reducir el log
        pass

def main():
    PORT = 8001
    
    with socketserver.TCPServer(("", PORT), CompraHandler) as httpd:
        print(f"Servidor de la lista de la compra corriendo en http://localhost:{PORT}")
        print("Presiona Ctrl+C para detener el servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido")

if __name__ == "__main__":
    main()
