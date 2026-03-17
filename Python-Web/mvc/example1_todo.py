"""
Example Application 1: Simple Todo List
Demonstrates framework separation - all framework code is in separate files.
"""

from controller import MVCServer


def home_handler(model, view, request):
    """Handle home page - display all todos."""
    todos = model.get('todos', [])
    
    # Generate HTML for todo items
    todo_items = ""
    if todos:
        for todo in todos:
            completed_class = 'completed' if todo.get('completed', False) else ''
            action_text = 'Desmarcar' if todo.get('completed', False) else 'Completar'
            
            todo_items += f"""
                <div class="todo-item {completed_class}">
                    <span class="todo-title">{todo['title']}</span>
                    <div class="todo-actions">
                        <a href="/toggle/{todo['id']}">{action_text}</a>
                        <a href="/delete/{todo['id']}" class="delete">Eliminar</a>
                    </div>
                </div>
            """
    else:
        todo_items = """
            <div class="empty-state">
                No hay tareas. ¡Añade una para empezar!
            </div>
        """
    
    return view.render_template('home.html', {'todos': todos, 'count': len(todos), 'todo_items': todo_items})


def add_todo_handler(model, view, request):
    """Handle adding a new todo."""
    if request['method'] == 'POST':
        title_list = request['post_data'].get('title', [])
        title = title_list[0] if title_list else ''
        if title.strip():
            todos = model.get('todos', [])
            new_todo = {'id': len(todos) + 1, 'title': title.strip(), 'completed': False}
            todos.append(new_todo)
            model.set('todos', todos)
            return view.redirect('/')
    return view.error_response(400, "Invalid todo title")


def delete_todo_handler(model, view, request):
    """Handle deleting a todo."""
    todo_id = int(request['path_params'].get('id', 0))
    todos = model.get('todos', [])
    todos = [todo for todo in todos if todo['id'] != todo_id]
    model.set('todos', todos)
    return view.redirect('/')


def toggle_todo_handler(model, view, request):
    """Handle toggling todo completion status."""
    todo_id = int(request['path_params'].get('id', 0))
    todos = model.get('todos', [])
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    model.set('todos', todos)
    return view.redirect('/')


def main():
    """Main function to set up and run the todo app."""
    # Create MVC server
    server = MVCServer(port=8001, storage_file="todo_app", templates_dir="todo_templates")
    
    # Add routes
    server.add_route('GET', '/', home_handler)
    server.add_route('POST', '/add', add_todo_handler)
    server.add_route('GET', '/delete/:id', delete_todo_handler)
    server.add_route('GET', '/toggle/:id', toggle_todo_handler)
    
    # Run server
    server.run()


if __name__ == "__main__":
    main()
