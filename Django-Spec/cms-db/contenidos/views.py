from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from .models import Contenido

@csrf_protect
def pagina_principal(request):
    if request.method == 'GET':
        # Get all resources
        recursos = Contenido.objects.all()
        
        # Build HTML
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Servidor de Contenidos</title>
        </head>
        <body>
            <h1>Servidor de Contenidos</h1>
            <p>Recursos disponibles:</p>
            <ul>
        """
        
        for recurso in recursos:
            html += f'                <li><a href="/{recurso.recurso}/">{recurso.recurso}</a></li>\n'
        
        # Get CSRF token
        csrf_token = get_token(request)
        
        html += f"""
            </ul>
            <h2>Crear nuevo recurso</h2>
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <p>
                    <label for="recurso">Nombre del recurso:</label><br>
                    <input type="text" name="recurso" id="recurso" required>
                </p>
                <p>
                    <label for="contenido">Contenido:</label><br>
                    <textarea name="contenido" id="contenido" rows="4" cols="50" required></textarea>
                </p>
                <p>
                    <input type="submit" value="Crear recurso">
                </p>
            </form>
        </body>
        </html>
        """
        
        return HttpResponse(html)
    
    elif request.method == 'POST':
        # Create new resource
        nombre_recurso = request.POST.get('recurso')
        contenido_texto = request.POST.get('contenido')
        
        if nombre_recurso and contenido_texto:
            Contenido.objects.create(recurso=nombre_recurso, contenido=contenido_texto)
        
        # Redirect to main page
        return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Recurso Creado</title>
        </head>
        <body>
            <h1>Recurso Creado</h1>
            <p>El recurso ha sido creado exitosamente.</p>
            <p><a href="/">Volver a la página principal</a></p>
        </body>
        </html>
        """)

def pagina_recurso(request, recurso):
    # Try to get the resource
    contenido_obj = get_object_or_404(Contenido, recurso=recurso)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{recurso.capitalize()}</title>
    </head>
    <body>
        <h1>{recurso.capitalize()}</h1>
        <p>{contenido_obj.contenido}</p>
        <p><a href="/">Volver a la página principal</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html)

def error_404(request, recurso):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error 404</title>
    </head>
    <body>
        <h1>Error 404</h1>
        <p>El recurso '{recurso}' no fue encontrado</p>
        <p><a href="/">Volver a la página principal</a></p>
    </body>
    </html>
    """
    
    return HttpResponse(html, status=404)
