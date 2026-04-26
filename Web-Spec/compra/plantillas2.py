# Plantillas HTML para la aplicación de lista de la compra (versión 2)

HTML_BASE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de la Compra</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .item-list {{
            list-style: none;
            padding: 0;
            margin: 20px 0;
        }}
        .item-list li {{
            padding: 15px;
            margin: 8px 0;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .item-list a {{
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            font-size: 18px;
        }}
        .item-list a:hover {{
            text-decoration: underline;
        }}
        .item-quantity {{
            color: #666;
            font-size: 16px;
            font-weight: bold;
        }}
        .form-container {{
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        .form-group {{
            margin-bottom: 15px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }}
        input[type="text"], input[type="number"] {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        button {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
        .quantity-display {{
            font-size: 24px;
            color: #333;
            margin: 20px 0;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 8px;
            text-align: center;
        }}
        .htmx-indicator {{
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .htmx-request .htmx-indicator {{
            opacity: 1;
        }}
        .htmx-request .htmx-indicator {{
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""

PAGINA_PRINCIPAL = """<h1>Lista de la Compra</h1>

<h2>Elementos en la lista</h2>
{lista_items}

<a href="/" class="back-link">← Actualizar lista</a>"""

PAGINA_ELEMENTO = """<h1>Elemento: {nombre}</h1>

<div class="quantity-display">
    Cantidad actual: <strong>{cantidad}</strong>
</div>

<div class="form-container">
    <h3>Actualizar cantidad</h3>
    <form method="POST" action="/{nombre}">
        <div class="form-group">
            <label for="valor">Nueva cantidad:</label>
            <input type="number" id="valor" name="valor" min="0" required>
        </div>
        <button type="submit" hx-put="/{nombre}" hx-target="body" hx-include="this">
            Actualizar cantidad
            <span class="htmx-indicator">⏳</span>
        </button>
    </form>
</div>

<a href="/" class="back-link">← Volver a la lista principal</a>"""

ITEM_LISTA_VACIA = "<p>No hay elementos en la lista de la compra.</p>"

ITEM_LISTA_CON_ELEMENTOS = """<ul class="item-list">
{items}
</ul>"""

ITEM_FORMATO = """<li>
    <a href="/{nombre}">{nombre}</a>
    <span class="item-quantity">Cantidad: {cantidad}</span>
</li>"""
