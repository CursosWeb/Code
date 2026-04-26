"""
Example Application 2: Simple Blog System
Demonstrates framework reusability with different application logic.
"""

from controller import MVCServer
import datetime


def home_handler(model, view, request):
    """Handle home page - display all blog posts."""
    posts = model.get('posts', [])
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Generate HTML for post items
    post_items = ""
    if posts:
        for post in posts:
            # Truncate content if too long
            content = post['content']
            if len(content) > 200:
                content = content[:200] + "..."
            
            post_items += f"""
                <div class="post-summary">
                    <h3 class="post-title">
                        <a href="/post/{post['id']}">{post['title']}</a>
                    </h3>
                    <div class="post-meta">
                        Por {post['author']} el {post['date']}
                    </div>
                    <div class="post-excerpt">
                        {content}
                    </div>
                    <div class="post-actions">
                        <a href="/delete/{post['id']}">Eliminar</a>
                    </div>
                </div>
            """
    else:
        post_items = """
            <div class="empty-state">
                No hay posts aún. ¡Sé el primero en escribir!
            </div>
        """
    
    return view.render_template('home.html', {'posts': posts, 'post_items': post_items})


def add_post_handler(model, view, request):
    """Handle adding a new blog post."""
    if request['method'] == 'POST':
        title_list = request['post_data'].get('title', [])
        content_list = request['post_data'].get('content', [])
        author_list = request['post_data'].get('author', [])
        
        title = title_list[0] if title_list else ''
        content = content_list[0] if content_list else ''
        author = author_list[0] if author_list else ''
        
        if title.strip() and content.strip():
            posts = model.get('posts', [])
            new_post = {
                'id': len(posts) + 1,
                'title': title.strip(),
                'content': content.strip(),
                'author': author.strip() or 'Anónimo',
                'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            posts.append(new_post)
            model.set('posts', posts)
            return view.redirect('/')
    return view.error_response(400, "Título y contenido son requeridos")


def view_post_handler(model, view, request):
    """Handle viewing a single blog post."""
    post_id = int(request['path_params'].get('id', 0))
    posts = model.get('posts', [])
    post = next((p for p in posts if p['id'] == post_id), None)
    
    if post:
        return view.render_template('post.html', {'post': post})
    else:
        return view.error_response(404, "Post no encontrado")


def delete_post_handler(model, view, request):
    """Handle deleting a blog post."""
    post_id = int(request['path_params'].get('id', 0))
    posts = model.get('posts', [])
    posts = [post for post in posts if post['id'] != post_id]
    model.set('posts', posts)
    return view.redirect('/')


def main():
    """Main function to set up and run the blog app."""
    # Create MVC server
    server = MVCServer(port=8002, storage_file="blog_app", templates_dir="blog_templates")
    
    # Add routes
    server.add_route('GET', '/', home_handler)
    server.add_route('POST', '/add', add_post_handler)
    server.add_route('GET', '/post/:id', view_post_handler)
    server.add_route('GET', '/delete/:id', delete_post_handler)
    
    # Run server
    server.run()


if __name__ == "__main__":
    main()
