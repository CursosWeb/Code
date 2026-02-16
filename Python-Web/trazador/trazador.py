from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json
import random
import string

class Trazador:
    def __init__(self):
        self.peticiones = []
    
    def generar_cookie(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def agregar_peticion(self, recurso, cookie):
        fecha_actual = datetime.now()
        self.peticiones.append((fecha_actual, recurso, cookie))
        return fecha_actual

# Crear instancia global del trazador
trazador = Trazador()

class TrazadorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extraer cookie "navegador" de la petición
        cookie_navegador = None
        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie'].split(';')
            for cookie in cookies:
                cookie = cookie.strip()
                if cookie.startswith('navegador='):
                    cookie_navegador = cookie[10:]  # Eliminar "navegador="
                    break
        
        # Si no hay cookie, generar una nueva
        nueva_cookie = False
        if cookie_navegador is None:
            cookie_navegador = trazador.generar_cookie()
            nueva_cookie = True

        if self.path == '/fechas.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            peticiones_formateadas = [
                {
                    'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    'recurso': recurso,
                    'cookie': cookie
                }
                for fecha, recurso, cookie in trazador.peticiones
            ]
            respuesta = {
                'total_peticiones': len(trazador.peticiones),
                'peticiones': peticiones_formateadas
            }
            self.wfile.write(json.dumps(respuesta).encode())
        elif self.path == '/fechas':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            if nueva_cookie:
                self.send_header('Set-Cookie', f'navegador={cookie_navegador}; HttpOnly')
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro de Peticiones</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Registro de Peticiones</h1>
    <p>Total de peticiones: {}</p>
    <table>
        <thead>
            <tr>
                <th>Nº</th>
                <th>Fecha y Hora</th>
                <th>Recurso</th>
                <th>Cookie</th>
            </tr>
        </thead>
        <tbody>
            {}
        </tbody>
    </table>
</body>
</html>
            """.format(
                len(trazador.peticiones),
                ''.join([
                    '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                        i+1, fecha.strftime("%Y-%m-%d %H:%M:%S"), recurso, cookie
                    )
                    for i, (fecha, recurso, cookie) in enumerate(trazador.peticiones)
                ])
            )
            
            self.wfile.write(html_content.encode())
        else:
            # Registrar la petición
            trazador.agregar_peticion(self.path, cookie_navegador)

            # Devolver imagen de 1x1 pixel transparente (GIF)
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            if nueva_cookie:
                self.send_header('Set-Cookie', f'navegador={cookie_navegador}; HttpOnly')
            self.end_headers()
            
            # GIF de 1x1 pixel transparente
            pixel_gif = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x04\x01\x00\x3b'
            self.wfile.write(pixel_gif)
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TrazadorHandler)
    print("Iniciando servidor trazador en http://localhost:8000")
    print("Endpoint principal: http://localhost:8000")
    print("Endpoint para ver fechas: http://localhost:8000/fechas")
    httpd.serve_forever()
