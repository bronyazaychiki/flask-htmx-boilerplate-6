from flask import Blueprint, render_template, request

bp = Blueprint('todos', __name__, url_prefix='/todos')

todos = [
    {'id': 1, 'name': 'Clean room', 'completed': True},
    {'id': 2, 'name': 'Buy groceries', 'completed': False},
    {'id': 3, 'name': 'Read a book', 'completed': True},
    {'id': 4, 'name': 'Write report', 'completed': False},
    {'id': 5, 'name': 'Call dentist', 'completed': False},
    {'id': 6, 'name': 'Fix the leaky faucet', 'completed': False},
]

_next_id = 7


def _get_status(source):
    """Read status from either the tab button name or the hidden _status input."""
    return source.get('status') or source.get('_status', 'all')


def _filter_todos(status='all', search=''):
    if status == 'pending':
        result = [t for t in todos if not t['completed']]
    elif status == 'completed':
        result = [t for t in todos if t['completed']]
    else:
        result = list(todos)

    if search:
        q = search.lower()
        result = [t for t in result if q in t['name'].lower()]

    return result


def _render_filtered(status, search):
    filtered = _filter_todos(status, search)
    counts = {
        'all': len(todos),
        'pending': len([t for t in todos if not t['completed']]),
        'completed': len([t for t in todos if t['completed']]),
    }
    return render_template("bp/todos/todos.html",
                           todos=filtered, counts=counts,
                           status=status, search=search)


@bp.route("/", methods=["GET"])
def get_todos():
    status = _get_status(request.args)
    search = request.args.get('search', '')
    return _render_filtered(status, search)


@bp.route("/add", methods=["POST"])
def add_todo():
    global _next_id
    todo_name = request.form.get("todo", "").strip()
    if todo_name:
        todos.append({'id': _next_id, 'name': todo_name, 'completed': False})
        _next_id += 1

    status = _get_status(request.form)
    search = request.form.get('search', '')
    return _render_filtered(status, search)


@bp.route("/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break

    status = _get_status(request.form)
    search = request.form.get('search', '')
    return _render_filtered(status, search)
