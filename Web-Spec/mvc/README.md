# MVC Framework para Python

Un framework web simple que implementa el patrón Modelo-Vista-Controlador (MVC) utilizando solo módulos de la biblioteca estándar de Python y `socketserver` directamente.

## Características

- **Modelo**: Gestión de estado con persistencia usando `shelve`
- **Vista**: Renderizado de plantillas HTML usando solo `format()` de Python
- **Controlador**: Servidor HTTP usando `socketserver` directamente (sin `http.server`)
- **Cookies**: Gestión completa de cookies HTTP (crear, extraer, enviar, eliminar)
- **Sesiones**: Gestión de sesiones HTTP con identificación por cookies
- **Sin dependencias externas**: Usa solo biblioteca estándar de Python
- **Separación completa**: La lógica de aplicación está completamente separada del framework

## Arquitectura

### Modelo (`model.py`)
- Gestiona el estado de la aplicación
- Proporciona persistencia usando `shelve`
- Operaciones: `get()`, `set()`, `delete()`, `exists()`, `clear()`, `update()`

### Vista (`view.py`)
- Renderiza plantillas HTML usando solo `format()` de Python
- Genera respuestas HTTP (HTML, JSON, redirecciones, errores)
- Procesa CSS con dobles llaves `{{}}` para evitar conflictos con variables de plantilla
- Sin sintaxis personalizada: solo sustitución de variables `{variable}`

### Controlador (`controller.py`)
- Servidor HTTP usando `socketserver` directamente
- Parseo manual de peticiones HTTP
- Enrutamiento explícito (sin decoradores)
- Coordinación entre modelo y vista

### Cookies (`cookies.py`)
- Gestión de cookies HTTP con atributos completos
- Soporte para cookies de sesión y persistentes
- Operaciones: crear, extraer de peticiones, enviar en respuestas, eliminar
- Atributos soportados: expires, max-age, domain, path, secure, httponly, samesite

### Sesiones (`sessions.py`)
- Gestión de sesiones HTTP usando cookies para identificación
- Soporte para timeout de sesiones y limpieza automática
- Operaciones: `get_session()`, `start_session()`, `update_session()`, `destroy_session()`
- Persistencia de datos de sesión usando el módulo Model

## Ejemplos de Aplicación

### 1. Lista de Tareas (Todo List)
```bash
python example1_todo.py
```
- Servidor en http://localhost:8001
- Funcionalidades: añadir, eliminar, marcar tareas como completadas

### 2. Blog Simple
```bash
python example2_blog.py
```
- Servidor en http://localhost:8002
- Funcionalidades: crear posts, ver posts individuales, eliminar posts

## Uso del Framework

### Crear una aplicación:

```python
from controller import MVCServer

def home_handler(model, view, request):
    # Lógica de aplicación
    data = model.get('key', 'default')
    return view.render_template('template.html', {'data': data})

def main():
    server = MVCServer(port=8080, storage_file="myapp", templates_dir="templates")
    
    # Añadir rutas (método HTTP, patrón URL, manejador)
    server.add_route('GET', '/', home_handler)
    server.add_route('POST', '/submit', submit_handler)
    
    server.run()

if __name__ == "__main__":
    main()
```

### Sistema de Enrutamiento

- **Rutas fijas**: `server.add_route('GET', '/about', about_handler)`
- **Parámetros de ruta**: `server.add_route('GET', '/user/:id', user_handler)`
- **Wildcards**: `server.add_route('GET', '/api/*', api_handler)`

### Manejadores de Ruta

Los manejadores reciben tres parámetros:
- `model`: Instancia del modelo para acceso a datos
- `view`: Instancia de la vista para renderizar
- `request`: Diccionario con información de la petición

```python
def handler(model, view, request):
    method = request['method']          # 'GET', 'POST', etc.
    path = request['path']              # '/user/123'
    path_params = request['path_params'] # {'id': '123'}
    query_params = request['query_params'] # {'key': 'value'}
    post_data = request['post_data']   # {'field': 'value'}
    headers = request['headers']        # {'User-Agent': '...'}
    
    # Lógica de aplicación
    return view.render_html("<h1>Hello</h1>")
```

### Plantillas HTML

Las plantillas usan solo la sintaxis de `format()` de Python para sustitución de variables:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0 auto;
            max-width: 800px;
        }}
        .highlight {{
            background-color: yellow;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
    <p>Total items: {count}</p>
</body>
</html>
```

**Nota importante**: 
- Para evitar conflictos entre las llaves de CSS y las variables de plantilla, usa dobles llaves `{{}}` en el CSS. El framework las convertirá automáticamente a llaves simples `{}`.
- Las plantillas solo soportan sustitución de variables con `{variable}`. No se permiten bucles, condicionales u otra sintaxis personalizada. La lógica compleja debe manejarse en el código Python antes de pasar los datos a la plantilla.

## Gestión de Cookies

El framework incluye un módulo completo para gestión de cookies HTTP:

### Crear Cookies

```python
from cookies import CookieManager, create_cookie

# Cookie simple
cookie = create_cookie('username', 'john_doe')

# Cookie con atributos
cookie = create_cookie(
    'session_id', 'abc123',
    expires=7,  # días
    path='/',
    httponly=True,
    secure=True,
    samesite='strict'
)

# Cookie de sesión (expira al cerrar navegador)
session_cookie = CookieManager.create_session_cookie('temp_data', 'value')

# Cookie persistente
persistent_cookie = CookieManager.create_persistent_cookie('user_pref', 'dark_mode', days=30)
```

### Extraer Cookies de Peticiones

```python
from cookies import extract_cookies

def handler(model, view, request):
    # Extraer todas las cookies del request
    cookies = extract_cookies(request['headers'])
    
    # Obtener cookie específica
    username = cookies.get('username', 'guest')
    
    return view.render_template('profile.html', {'username': username})
```

### Enviar Cookies en Respuestas

```python
from cookies import set_cookie

def login_handler(model, view, request):
    # Lógica de login...
    
    # Crear cookie de sesión
    session_cookie = create_cookie('session_id', 'new_session_id', httponly=True)
    
    # Obtener headers para establecer la cookie
    cookie_headers = set_cookie(session_cookie)
    
    # Combinar con respuesta HTML
    html_response = view.render_template('dashboard.html', {'user': 'john'})
    
    # Añadir headers de cookie a la respuesta
    response = html_response.decode('utf-8')
    for header_name, header_value in cookie_headers.items():
        response = response.replace('HTTP/1.1 200 OK', f'HTTP/1.1 200 OK\r\n{header_name}: {header_value}')
    
    return response.encode('utf-8')
```

### Eliminar Cookies

```python
from cookies import delete_cookie

def logout_handler(model, view, request):
    # Crear headers para eliminar cookie
    delete_headers = delete_cookie('session_id', path='/')
    
    # Redirección con eliminación de cookie
    redirect_response = view.redirect('/login')
    
    # Añadir headers de eliminación
    response = redirect_response.decode('utf-8')
    for header_name, header_value in delete_headers.items():
        response = response.replace('HTTP/1.1 302 Found', f'HTTP/1.1 302 Found\r\n{header_name}: {header_value}')
    
    return response.encode('utf-8')
```

## Gestión de Sesiones

El framework incluye gestión de sesiones HTTP usando cookies para identificación:

### Iniciar Sesión

```python
from sessions import start_session

def login_handler(model, view, request):
    # Lógica de autenticación...
    if authenticated:
        # Iniciar sesión con datos iniciales
        session_data, cookie_headers = start_session({
            'username': 'john_doe',
            'role': 'user',
            'login_time': time.time()
        })
        
        # Respuesta con cookie de sesión
        html_response = view.render_template('dashboard.html', session_data)
        
        # Añadir headers de cookie
        response = html_response.decode('utf-8')
        for header_name, header_value in cookie_headers.items():
            response = response.replace('HTTP/1.1 200 OK', f'HTTP/1.1 200 OK\r\n{header_name}: {header_value}')
        
        return response.encode('utf-8')
```

### Obtener Sesión

```python
from sessions import get_session

def profile_handler(model, view, request):
    # Obtener datos de sesión
    session_data = get_session(request['headers'])
    
    if session_data:
        # Usuario tiene sesión activa
        return view.render_template('profile.html', {
            'username': session_data.get('username', 'Unknown'),
            'role': session_data.get('role', 'guest')
        })
    else:
        # No hay sesión activa
        return view.redirect('/login')
```

### Actualizar Sesión

```python
from sessions import update_session

def update_preferences_handler(model, view, request):
    # Actualizar datos de sesión
    updated_session = update_session(request['headers'], {
        'theme': 'dark',
        'language': 'es'
    })
    
    if updated_session:
        return view.render_template('settings.html', updated_session)
    else:
        return view.redirect('/login')
```

### Eliminar Sesión

```python
from sessions import destroy_session

def logout_handler(model, view, request):
    # Eliminar sesión y obtener headers de eliminación
    delete_headers = destroy_session(request['headers'])
    
    # Redirección con eliminación de cookie
    redirect_response = view.redirect('/login')
    
    # Añadir headers de eliminación
    response = redirect_response.decode('utf-8')
    for header_name, header_value in delete_headers.items():
        response = response.replace('HTTP/1.1 302 Found', f'HTTP/1.1 302 Found\r\n{header_name}: {header_value}')
    
    return response.encode('utf-8')
```

### Configuración de Sesiones

```python
from sessions import set_session_timeout, cleanup_sessions

# Configurar timeout de sesión (2 horas)
set_session_timeout(7200)

# Limpiar sesiones expiradas (se puede llamar periódicamente)
cleanup_sessions()
```

## Implementación Técnica

### HTTP Server Directo

El framework implementa un servidor HTTP usando `socketserver.BaseRequestHandler` directamente:

- Parseo manual de líneas de petición HTTP
- Extracción de headers y body
- Construcción manual de respuestas HTTP
- Manejo de diferentes métodos HTTP (GET, POST, PUT, DELETE)

### Persistencia con Shelve

- Usa `shelve` para persistencia de datos
- Almacenamiento en archivos binarios
- Acceso tipo diccionario a datos persistentes

## Verificación de Separación

Las dos aplicaciones de ejemplo demuestran que:
1. Todo el código común está en los archivos del framework (`model.py`, `view.py`, `controller.py`, `cookies.py`, `sessions.py`)
2. Las aplicaciones usan el mismo framework con lógica completamente diferente
3. No hay código de aplicación mezclado con el framework
4. El framework usa `socketserver` directamente sin `http.server`
5. El módulo de cookies proporciona gestión completa de cookies HTTP sin dependencias externas
6. El módulo de sesiones implementa gestión de sesiones HTTP con identificación por cookies

## Requisitos

- Python 3.6+
- Sin dependencias externas (solo biblioteca estándar)

## Licencia

Este framework es para propósitos educativos y demostrativos.
