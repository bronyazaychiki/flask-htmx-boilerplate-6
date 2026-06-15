from flask import Blueprint, render_template, request, current_app as app

bp = Blueprint('todos', __name__, url_prefix='/todos')

todos = [{'id': 1, 'name': 'Clean room', 'done': False}]


def _stats():
    return {
        'total': len(todos),
        'pending': len([t for t in todos if not t['done']]),
        'completed': len([t for t in todos if t['done']]),
    }


def _next_id():
    return max((t['id'] for t in todos), default=0) + 1


@bp.route("/", methods=["GET"])
def get_todos():
    return render_template("bp/todos/todos.html", todos=todos, stats=_stats())


@bp.route("/add", methods=["POST"])
def add_todo():
    todo_name = request.form.get("todo", "").strip()
    if not todo_name:
        return '', 400

    todos.append({'id': _next_id(), 'name': todo_name, 'done': False})
    return render_template("bp/todos/todos.html", todos=todos, stats=_stats())


@bp.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            break
    return render_template("bp/todos/todos.html", todos=todos, stats=_stats())


@bp.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return render_template("bp/todos/todos.html", todos=todos, stats=_stats())


