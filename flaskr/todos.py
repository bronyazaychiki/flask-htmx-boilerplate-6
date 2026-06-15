from flask import Blueprint, render_template, request, make_response

bp = Blueprint('todos', __name__, url_prefix='/todos')

todos = [{'id': 1, 'name': 'Clean room', 'completed': False}]


def next_id():
    return max((t['id'] for t in todos), default=0) + 1


def trigger_refresh():
    resp = make_response('')
    resp.headers['HX-Trigger'] = 'todos-updated'
    return resp


@bp.route("/", methods=["GET"])
def get_todos():
    return render_template("bp/todos/todos.html", todos=todos)


@bp.route("/add", methods=["POST"])
def add_todo():
    todo_name = request.form.get("todo")
    if todo_name:
        todos.append({'id': next_id(), 'name': todo_name, 'completed': False})
    return render_template("bp/todos/todos.html", todos=todos)


@bp.route("/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    return trigger_refresh()


@bp.route("/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    todos[:] = [t for t in todos if t['id'] != todo_id]
    return trigger_refresh()


@bp.route("/bulk-complete", methods=["POST"])
def bulk_complete():
    ids = [int(x) for x in request.form.getlist('todo_ids')]
    for todo in todos:
        if todo['id'] in ids:
            todo['completed'] = True
    return trigger_refresh()


@bp.route("/bulk-restore", methods=["POST"])
def bulk_restore():
    ids = [int(x) for x in request.form.getlist('todo_ids')]
    for todo in todos:
        if todo['id'] in ids:
            todo['completed'] = False
    return trigger_refresh()


@bp.route("/bulk-delete", methods=["POST"])
def bulk_delete():
    ids = [int(x) for x in request.form.getlist('todo_ids')]
    todos[:] = [t for t in todos if t['id'] not in ids]
    return trigger_refresh()
