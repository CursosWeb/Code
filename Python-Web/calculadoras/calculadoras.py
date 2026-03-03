#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import uuid
import sys
import argparse
from http import HTTPStatus

# Estado compartido
calculadoras = {}

class CalculadorasHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.handle_main_page()
        elif self.path.startswith('/calcs/'):
            self.handle_calculator_get()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Página no encontrada")
    
    def do_POST(self):
        if self.path == '/':
            self.handle_create_calculator()
        elif self.path.startswith('/calcs/'):
            self.handle_calculator_post()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Página no encontrada")
    
    def handle_main_page(self):
        """GET / - Página principal con formulario para crear calculadora"""
        # Generar listado de calculadoras existentes
        calculadoras_html = ""
        if calculadoras:
            calculadoras_html = "<h2>Calculadoras existentes:</h2><ul>"
            for calc_id, calc_data in calculadoras.items():
                calc_tipo = calc_data['tipo']
                calculadoras_html += f'<li><a href="/calcs/{calc_id}">Calculadora {calc_id}</a> - Tipo: {calc_tipo}</li>'
            calculadoras_html += "</ul>"
        else:
            calculadoras_html = "<p>No hay calculadoras creadas aún.</p>"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadoras</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadoras</h1>
    <form method="POST" action="/">
        <label for="tipo">Tipo de calculadora:</label>
        <select id="tipo" name="crear">
            <option value="iva">Calculadora de IVA</option>
            <option value="suma">Calculadora de Sumas</option>
        </select>
        <button type="submit">Crear Nueva Calculadora</button>
    </form>
    
    {calculadoras_html}
</body>
</html>
"""
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_create_calculator(self):
        """POST / - Crear nueva calculadora"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        if 'crear' in params and params['crear'][0] in ['iva', 'suma']:
            calc_tipo = params['crear'][0]
            # Generar ID único
            calc_id = str(uuid.uuid4())[:8]  # Usar primeros 8 caracteres del UUID
            calculadoras[calc_id] = {'tipo': calc_tipo, 'valor': None}
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora Creada</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadora Creada</h1>
    <p>Tu calculadora de tipo <strong>{calc_tipo}</strong> ha sido creada con ID: <strong>{calc_id}</strong></p>
    <p><a href="/calcs/{calc_id}">Ir a la calculadora</a></p>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
"""
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(HTTPStatus.BAD_REQUEST, "Tipo de calculadora no válido")
    
    def handle_calculator_get(self):
        """GET /calcs/<id> - Mostrar formulario de calculadora específica"""
        # Extraer ID del path
        path_parts = self.path.split('/')
        if len(path_parts) != 3:
            self.send_error(HTTPStatus.NOT_FOUND, "ID de calculadora no válido")
            return
        
        calc_id = path_parts[2]
        
        if calc_id not in calculadoras:
            self.send_error(HTTPStatus.NOT_FOUND, "Calculadora no encontrada")
            return
        
        calc_data = calculadoras[calc_id]
        calc_tipo = calc_data['tipo']
        
        if calc_tipo == 'iva':
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora {calc_id}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadora de IVA - ID: {calc_id}</h1>
    <form method="POST" action="/calcs/{calc_id}">
        <label for="valor">Cantidad para calcular IVA:</label>
        <input type="number" id="valor" name="valor" step="0.01" required>
        <button type="submit">Calcular IVA</button>
    </form>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
"""
        elif calc_tipo == 'suma':
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora {calc_id}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadora de Sumas - ID: {calc_id}</h1>
    <form method="POST" action="/calcs/{calc_id}">
        <label for="sum1">Primer número:</label>
        <input type="number" id="sum1" name="sum1" step="0.01" required>
        <br><br>
        <label for="sum2">Segundo número:</label>
        <input type="number" id="sum2" name="sum2" step="0.01" required>
        <br><br>
        <button type="submit">Calcular Suma</button>
    </form>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
"""
        else:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Tipo de calculadora no reconocido")
            return
        
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_calculator_post(self):
        """POST /calcs/<id> - Calcular operación y actualizar estado"""
        # Extraer ID del path
        path_parts = self.path.split('/')
        if len(path_parts) != 3:
            self.send_error(HTTPStatus.NOT_FOUND, "ID de calculadora no válido")
            return
        
        calc_id = path_parts[2]
        
        if calc_id not in calculadoras:
            self.send_error(HTTPStatus.NOT_FOUND, "Calculadora no encontrada")
            return
        
        calc_data = calculadoras[calc_id]
        calc_tipo = calc_data['tipo']
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        if calc_tipo == 'iva':
            if 'valor' not in params:
                self.send_error(HTTPStatus.BAD_REQUEST, "Valor no proporcionado")
                return
            
            try:
                valor = float(params['valor'][0])
                # Calcular IVA (21% en España)
                iva = valor * 0.21
                
                # Actualizar estado
                calculadoras[calc_id]['valor'] = valor
                
                html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora {calc_id}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadora de IVA - ID: {calc_id}</h1>
    <h2>Resultado</h2>
    <p>Cantidad original: <strong>{valor:.2f}€</strong></p>
    <p>IVA (21%): <strong>{iva:.2f}€</strong></p>
    <p>Total con IVA: <strong>{valor + iva:.2f}€</strong></p>
    
    <h3>Calcular otra cantidad</h3>
    <form method="POST" action="/calcs/{calc_id}">
        <label for="valor">Cantidad para calcular IVA:</label>
        <input type="number" id="valor" name="valor" step="0.01" required>
        <button type="submit">Calcular IVA</button>
    </form>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
"""
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
                
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Valor numérico no válido")
                
        elif calc_tipo == 'suma':
            if 'sum1' not in params or 'sum2' not in params:
                self.send_error(HTTPStatus.BAD_REQUEST, "Valores no proporcionados")
                return
            
            try:
                sum1 = float(params['sum1'][0])
                sum2 = float(params['sum2'][0])
                resultado = sum1 + sum2
                
                # Actualizar estado
                calculadoras[calc_id]['valor'] = (sum1, sum2)
                
                html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Calculadora {calc_id}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Calculadora de Sumas - ID: {calc_id}</h1>
    <h2>Resultado</h2>
    <p>Primer número: <strong>{sum1:.2f}</strong></p>
    <p>Segundo número: <strong>{sum2:.2f}</strong></p>
    <p>Suma: <strong>{resultado:.2f}</strong></p>
    
    <h3>Calcular otra suma</h3>
    <form method="POST" action="/calcs/{calc_id}">
        <label for="sum1">Primer número:</label>
        <input type="number" id="sum1" name="sum1" step="0.01" required>
        <br><br>
        <label for="sum2">Segundo número:</label>
        <input type="number" id="sum2" name="sum2" step="0.01" required>
        <br><br>
        <button type="submit">Calcular Suma</button>
    </form>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
"""
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
                
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "Valores numéricos no válidos")
        else:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Tipo de calculadora no reconocido")

def run_server(port=8000):
    with socketserver.TCPServer(("", port), CalculadorasHandler) as httpd:
        print(f"Servidor iniciado en http://localhost:{port}")
        print("Presiona Ctrl+C para detener el servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor de calculadoras')
    parser.add_argument('port', nargs='?', type=int, default=8000, 
                       help='Puerto en el que lanzar el servidor HTTP (default: 8000)')
    args = parser.parse_args()
    
    run_server(args.port)
