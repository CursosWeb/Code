#!/usr/bin/env python3
import http.server
import http.cookies
import urllib.parse
import secrets

class SessionHandler(http.server.BaseHTTPRequestHandler):
    
    # Simulamos una base de datos de usuarios (usuario: password)
    USERS = {
        'admin': 'admin123',
        'user': 'password',
        'test': 'test123'
    }
    
    # Almacenamiento de sesiones en memoria (session_id: username)
    sessions = {}
    
    # Almacenamiento de objetos por usuario (username: [objetos])
    user_objects = {}
    
    def do_GET(self):
        if self.path == '/':
            self.handle_main_page()
        elif self.path == '/logout':
            self.handle_logout()
        elif self.path == '/objetos':
            self.handle_objetos_page()
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        if self.path == '/':
            self.handle_login()
        elif self.path == '/objetos':
            self.handle_add_objeto()
        else:
            self.send_error(404, "File not found")
    
    def handle_main_page(self):
        # Verificar si existe una cookie de sesión
        session_id = self.get_session_id_from_cookie()
        
        if session_id and session_id in self.sessions:
            # Usuario ya logeado
            username = self.sessions[session_id]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Usuario Logeado</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 50px; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .success {{ color: green; font-size: 24px; }}
                    .logout {{ margin-top: 20px; }}
                    .nav {{ margin-top: 30px; }}
                    .nav a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
                    .nav a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="success">Usuario logeado</h1>
                    <p>Bienvenido, <strong>{username}</strong>!</p>
                    <p>Has iniciado sesión correctamente.</p>
                    <div class="nav">
                        <a href="/objetos">Gestionar Objetos</a>
                        <a href="/logout">Cerrar sesión</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            # Mostrar formulario de login
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 50px; }
                    .container { max-width: 400px; margin: 0 auto; }
                    .form-group { margin-bottom: 15px; }
                    label { display: block; margin-bottom: 5px; }
                    input[type="text"], input[type="password"] { 
                        width: 100%; padding: 8px; border: 1px solid #ccc; 
                        border-radius: 4px; box-sizing: border-box;
                    }
                    button { 
                        background-color: #007bff; color: white; padding: 10px 20px; 
                        border: none; border-radius: 4px; cursor: pointer;
                    }
                    button:hover { background-color: #0056b3; }
                    .error { color: red; margin-top: 10px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Iniciar Sesión</h1>
                    <form method="POST" action="/">
                        <div class="form-group">
                            <label for="username">Usuario:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Contraseña:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit">Iniciar Sesión</button>
                    </form>
                    <p><small>Usuarios de prueba: admin/admin123, user/password, test/test123</small></p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
    
    def handle_login(self):
        # Obtener datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(post_data)
        
        username = form_data.get('username', [''])[0]
        password = form_data.get('password', [''])[0]
        
        # Verificar credenciales
        if username in self.USERS and self.USERS[username] == password:
            # Crear sesión
            session_id = secrets.token_hex(16)
            self.sessions[session_id] = username
            
            # Enviar cookie de sesión
            self.send_response(302)  # Redirect
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly; Path=/')
            self.end_headers()
        else:
            # Credenciales incorrectas
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login Error</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 50px; }
                    .container { max-width: 400px; margin: 0 auto; }
                    .error { color: red; font-size: 18px; }
                    .form-group { margin-bottom: 15px; }
                    label { display: block; margin-bottom: 5px; }
                    input[type="text"], input[type="password"] { 
                        width: 100%; padding: 8px; border: 1px solid #ccc; 
                        border-radius: 4px; box-sizing: border-box;
                    }
                    button { 
                        background-color: #007bff; color: white; padding: 10px 20px; 
                        border: none; border-radius: 4px; cursor: pointer;
                    }
                    button:hover { background-color: #0056b3; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Iniciar Sesión</h1>
                    <p class="error">Usuario o contraseña incorrectos</p>
                    <form method="POST" action="/login">
                        <div class="form-group">
                            <label for="username">Usuario:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Contraseña:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit">Iniciar Sesión</button>
                    </form>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
    
    def handle_logout(self):
        # Obtener session_id de la cookie
        session_id = self.get_session_id_from_cookie()
        
        # Eliminar la sesión si existe
        if session_id and session_id in self.sessions:
            del self.sessions[session_id]
        
        # Enviar cookie vacía para eliminar la del cliente y redirigir
        self.send_response(302)  # Redirect
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', 'session_id=; HttpOnly; Path=/; Max-Age=0')
        self.end_headers()
    
    def handle_objetos_page(self):
        # Verificar si existe una cookie de sesión
        session_id = self.get_session_id_from_cookie()
        
        if not session_id or session_id not in self.sessions:
            # Redirigir al login si no está logeado
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
        
        username = self.sessions[session_id]
        
        # Obtener objetos del usuario
        objetos = self.user_objects.get(username, [])
        
        # Generar HTML de la lista de objetos
        objetos_html = ""
        if objetos:
            objetos_html = "<h3>Tus Objetos:</h3><ul>"
            for i, obj in enumerate(objetos):
                objetos_html += f"<li>{obj}</li>"
            objetos_html += "</ul>"
        else:
            objetos_html = "<p>No tienes objetos aún. ¡Añade tu primer objeto!</p>"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gestionar Objetos</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .form-group {{ margin-bottom: 15px; }}
                label {{ display: block; margin-bottom: 5px; }}
                input[type="text"] {{ 
                    width: 100%; padding: 8px; border: 1px solid #ccc; 
                    border-radius: 4px; box-sizing: border-box;
                }}
                button {{ 
                    background-color: #007bff; color: white; padding: 10px 20px; 
                    border: none; border-radius: 4px; cursor: pointer;
                }}
                button:hover {{ background-color: #0056b3; }}
                .objetos-list {{ margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 4px; }}
                .nav {{ margin-bottom: 30px; }}
                .nav a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
                .nav a:hover {{ text-decoration: underline; }}
                ul {{ list-style-type: disc; margin-left: 20px; }}
                li {{ margin-bottom: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav">
                    <a href="/">Inicio</a>
                    <a href="/logout">Cerrar sesión</a>
                </div>
                <h1>Gestionar Objetos</h1>
                <p>Bienvenido, <strong>{username}</strong></p>
                
                <h2>Añadir Nuevo Objeto</h2>
                <form method="POST" action="/objetos">
                    <div class="form-group">
                        <label for="objeto">Nombre del objeto:</label>
                        <input type="text" id="objeto" name="objeto" required placeholder="Ej: Libro, Silla, Ordenador...">
                    </div>
                    <button type="submit">Añadir Objeto</button>
                </form>
                
                <div class="objetos-list">
                    {objetos_html}
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def handle_add_objeto(self):
        # Verificar si existe una cookie de sesión
        session_id = self.get_session_id_from_cookie()
        
        if not session_id or session_id not in self.sessions:
            # Redirigir al login si no está logeado
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
        
        username = self.sessions[session_id]
        
        # Obtener datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(post_data)
        
        objeto = form_data.get('objeto', [''])[0].strip()
        
        if objeto:
            # Inicializar lista de objetos del usuario si no existe
            if username not in self.user_objects:
                self.user_objects[username] = []
            
            # Añadir objeto a la lista del usuario
            self.user_objects[username].append(objeto)
        
        # Redirigir de vuelta a la página de objetos
        self.send_response(302)
        self.send_header('Location', '/objetos')
        self.end_headers()
    
    def get_session_id_from_cookie(self):
        # Obtener cookies del header
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None
        
        # Parsear cookies
        cookies = http.cookies.SimpleCookie()
        cookies.load(cookie_header)
        
        # Obtener session_id
        if 'session_id' in cookies:
            return cookies['session_id'].value
        return None

def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, SessionHandler)
    print(f"Servidor iniciado en http://localhost:8000")
    print("Presiona Ctrl+C para detener el servidor")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
