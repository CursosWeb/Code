## Eliminación de fondo en fotos

Elimina los planos de fondo (background) de una foto: [background.py](background.py)

* Dependencias: [rembg](https://github.com/danielgatis/rembg)

```commandline
pip install rembg[cli]
```

* Otros detalles de instalación: La primera vez que se ejecuta, puede que el módulo `rembg` trate de descargarse el modelo de aprendizaje automático (machine learning) que utiliza. Su descarga puede fallar, porque se almacena en Google Drive, que tiene limitaciones para descarga. Si eso ocurre, se verá un error que incluye algo como:

```
Access denied with the following error:
...
You may still be able to access the file from the browser:

         https://drive.google.com/uc?id=1tCU5MM1LhRgGou5OpmpjBQbSrYIUoYab 

Traceback (most recent call last):
...
[...] Load model from ~/.u2net/u2net.onnx failed. File doesn't exist
```

Si esto ocurre, podemos descargar el fichero de modelo (`u2net.onnx`) manualmente, desde el navegador, y copiarlo al directorio donde `remgb` espera encontrarlo (`~/.u2net`). Por ejemplo, si se ha descargado a `~/Downloads`:

```commandline
cp ~/Downloads/u2net.onnx ~/.u2net/u2net.onnx
```

* Uso desde línea de comandos:

```commandline
rembg i cafe.jpg cafe-nobg.jpg
```

* Explicación detallada: [How to Remove Image Background Using Python](https://python.plainenglish.io/how-to-remove-image-background-using-python-6f7ffa8eab15)
