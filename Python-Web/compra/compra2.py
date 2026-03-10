#!/usr/bin/env python3

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import plantillas2

# Estado: diccionario para almacenar la lista de la compra
compra = {}

class Compra2Handler(http.server.BaseHTTPRequestHandler):
    
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
                    items_html += plantillas2.ITEM_FORMATO.format(
                        nombre=nombre, 
                        cantidad=cantidad
                    )
                lista_html = plantillas2.ITEM_LISTA_CON_ELEMENTOS.format(items=items_html)
            else:
                lista_html = plantillas2.ITEM_LISTA_VACIA
            
            content = plantillas2.PAGINA_PRINCIPAL.format(lista_items=lista_html)
            page = plantillas2.HTML_BASE.format(content=content)
            
            self.wfile.write(page.encode('utf-8'))
            
        else:
            # GET /<elemento> - Página de un elemento específico
            elemento = path
            cantidad = compra.get(elemento, 0)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            content = plantillas2.PAGINA_ELEMENTO.format(
                nombre=elemento,
                cantidad=cantidad
            )
            page = plantillas2.HTML_BASE.format(content=content)
            
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
            
            # Redirigir a GET / (mostrar la página principal)
            self.do_GET()
            
        else:
            # POST /<elemento> - Para compatibilidad con formularios tradicionales
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
    
    def do_PUT(self):
        # PUT /<elemento> - Actualizar cantidad de un elemento
        parsed_path = urlparse(self.path)
        path = parsed_path.path.strip('/')
        
        if path:  # Solo procesar PUT para elementos específicos
            elemento = path
            
            # Leer el cuerpo de la petición
            content_length = int(self.headers.get('Content-Length', 0))
            put_data = self.rfile.read(content_length).decode('utf-8').strip()
            
            # El cuerpo contiene directamente la cantidad
            try:
                nueva_cantidad = int(put_data)
                if nueva_cantidad >= 0:
                    compra[elemento] = nueva_cantidad
            except ValueError:
                pass  # Ignorar valores no válidos
            
            # Devolver la página actualizada del elemento
            cantidad = compra.get(elemento, 0)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            content = plantillas2.PAGINA_ELEMENTO.format(
                nombre=elemento,
                cantidad=cantidad
            )
            page = plantillas2.HTML_BASE.format(content=content)
            
            self.wfile.write(page.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Sobreescribir para reducir el log
        pass

def main():
    PORT = 8002  # Puerto diferente para evitar conflictos
    
    with socketserver.TCPServer(("", PORT), Compra2Handler) as httpd:
        print(f"Servidor de la lista de la compra v2 corriendo en http://localhost:{PORT}")
        print("Presiona Ctrl+C para detener el servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido")

if __name__ == "__main__":
    main()
