import base64
from django.http import HttpResponse
import random
import urllib.request

page = """
<!DOCTYPE html>
<html lang='en'>
  <head>
    <script src='https://unpkg.com/htmx.org@1.9.10'></script>
  </head>
  <body>
  <p>Loading HTML image every 3 seconds</p>
  <div hx-get="/image_embedded" 
    hx-trigger="load, change, every 3s"    
    hx-target='#content_embedded'
    hx-swap='innerHTML'>
    </div>
    <div id='content_embedded'></div> 

  <p>Loading bytes image every 3 seconds</p>
  <div hx-get="/image_html" 
    hx-trigger="load, change, every 3s"    
    hx-target='#content_html'
    hx-swap='innerHTML'>
    </div>
    <div id='content_html'></div> 
  </body>
</html>
"""

# URL de la imagen a descargar
url_imagen = "https://ctraficomovilidad.malaga.eu/recursos/movilidad/camaras_trafico/TV-24.jpg"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
}


def download_image():
    """Download image and return it as bytes"""
    request = urllib.request.Request(url=url_imagen, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            image = response.read()
    except urllib.error.URLError as e:
        return None
    return image

def image(request):
    """Return the image as bytes"""
    image = download_image()
    if image is None:
        return HttpResponse(str(e), status=500)
    else:
        return HttpResponse(image, content_type="image/jpeg")

def image_html(request):
    """Return HTML text, with a IMG element referencing the image"""
    html=f'<img src="/image?{random.randrange(10000)}">'
    return HttpResponse(html, content_type="text/html")

def image_embedded(request):
    """Return HTML text, with a IMG element embedding the image"""
    image = download_image()
    if image is None:
        return HttpResponse(str(e), status=500)
    else:
        image_base64 = base64.b64encode(image).decode('utf-8')
        html=f'<img src="data:image/jpeg;base64,{image_base64}">'
        return HttpResponse(html, content_type="text/html")

def main(request):
    if request.method =="GET":
        return HttpResponse(page)
