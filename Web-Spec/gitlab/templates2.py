# HTML Templates for GitLab Repository Viewer (server2.py)

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitLab Repository Viewer</title>
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
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        input[type="text"]:focus {{
            border-color: #fc6d26;
            outline: none;
        }}
        button {{
            background-color: #fc6d26;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }}
        button:hover {{
            background-color: #e55100;
        }}
        .example {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 GitLab Repository Viewer</h1>
        
        <form method="GET" action="/">
            <div class="form-group">
                <label for="repo">Nombre del repositorio:</label>
                <input type="text" id="repo" name="repo" 
                       placeholder="ej: cursoprogram/bifurca-repositorio" 
                       value="cursoprogram/bifurca-repositorio" required>
                <div class="example">Formato: grupo/proyecto</div>
            </div>
            <button type="submit">Ver Repositorio</button>
        </form>
    </div>
</body>
</html>
"""

REPO_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Issues - {repo_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        .stat {{
            background-color: #f8f9fa;
            padding: 10px 15px;
            border-radius: 5px;
            border-left: 4px solid #fc6d26;
        }}
        .back-link {{
            color: #fc6d26;
            text-decoration: none;
            font-weight: bold;
        }}
        .issue {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #fc6d26;
        }}
        .issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .issue-number {{
            background-color: #6c757d;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}
        .issue-state.opened {{
            color: #28a745;
            font-weight: bold;
        }}
        .issue-state.closed {{
            color: #dc3545;
            font-weight: bold;
        }}
        .issue-title {{
            margin: 10px 0;
            color: #333;
        }}
        .issue-description {{
            color: #666;
            line-height: 1.5;
            margin: 10px 0;
        }}
        .issue-meta a {{
            color: #fc6d26;
            text-decoration: none;
            font-weight: bold;
        }}
        .issue-meta a:hover {{
            text-decoration: underline;
        }}
        .new-issue-form {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-left: 4px solid #28a745;
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
        input[type="text"], textarea {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }}
        textarea {{
            height: 100px;
            resize: vertical;
        }}
        input[type="text"]:focus, textarea:focus {{
            border-color: #fc6d26;
            outline: none;
        }}
        .btn {{
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
        }}
        .btn:hover {{
            background-color: #218838;
        }}
        .no-issues {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}
        .error {{
            color: #d9534f;
            background-color: #f9f2f2;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #d9534f;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Issues de <code>{repo_name}</code></h1>
        <div class="stats">
            <div class="stat">
                <strong>Total:</strong> {total_issues}
            </div>
            <div class="stat">
                <strong>🟢 Abiertos:</strong> {open_issues}
            </div>
            <div class="stat">
                <strong>🔴 Cerrados:</strong> {closed_issues}
            </div>
        </div>
        <div style="margin-top: 15px;">
            <a href="/" class="back-link">← Volver al inicio</a>
        </div>
    </div>
    
    {error_message}
    
    <div class="new-issue-form">
        <h2>➕ Crear Nuevo Issue</h2>
        <form method="POST">
            <div class="form-group">
                <label for="title">Título:</label>
                <input type="text" id="title" name="title" required>
            </div>
            <div class="form-group">
                <label for="description">Descripción:</label>
                <textarea id="description" name="description"></textarea>
            </div>
            <button type="submit" class="btn">Crear Issue</button>
        </form>
    </div>
    
    {issues_html}
</body>
</html>
"""

ISSUE_ITEM_TEMPLATE = """
<div class="issue">
    <div class="issue-header">
        <span class="issue-number">#{issue_number}</span>
        <span class="issue-state {state}">{state_icon} {state_text}</span>
    </div>
    <h3 class="issue-title">{title}</h3>
    <p class="issue-description">{description}</p>
    <div class="issue-meta">
        <a href="{web_url}" target="_blank">Ver en GitLab →</a>
    </div>
</div>
"""
