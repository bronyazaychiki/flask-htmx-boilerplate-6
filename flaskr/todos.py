from flask import Blueprint, render_template, request

bp = Blueprint('todos', __name__, url_prefix='/todos')

todos = [{'id': 1, 'name': 'Clean room', 'completed': False}]
_next_id = 2


def _generate_id():
    global _next_id
    id_val = _next_id
    _next_id += 1
    return id_val


def _find_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    return None


def _validate_name(raw):
    if raw is None:
        return None, 'Todo name cannot be empty'
    cleaned = raw.strip()
    if not cleaned:
        return None, 'Todo name cannot be empty'
    if len(cleaned) > 200:
        return None, 'Todo name is too long (max 200 characters)'
    return cleaned, None


def _toast(message, error=False):
    return render_template('bp/todos/toast.html', message=message, error=error)


@bp.route("/", methods=["GET"])
def get_todos():
    return render_template("bp/todos/todos.html", todos=todos)


@bp.route("/add", methods=["POST"])
def add_todo():
    todo_name, err = _validate_name(request.form.get("todo"))
    if err:
        return render_template("bp/todos/todos.html", todos=todos) + _toast(err, error=True)

    todos.append({'id': _generate_id(), 'name': todo_name, 'completed': False})
    return render_template("bp/todos/todos.html", todos=todos) + _toast("Todo added!")


@bp.route("/<int:todo_id>/edit", methods=["GET"])
def edit(todo_id):
    todo = _find_todo(todo_id)
    if not todo:
        return _toast("Todo not found", error=True)
    return render_template("bp/todos/row_edit.html", todo=todo)


@bp.route("/<int:todo_id>/display", methods=["GET"])
def display(todo_id):
    todo = _find_todo(todo_id)
    if not todo:
        return _toast("Todo not found", error=True)
    return render_template("bp/todos/row_display.html", todo=todo)


@bp.route("/<int:todo_id>/save", methods=["POST"])
def save(todo_id):
    todo = _find_todo(todo_id)
    if not todo:
        return _toast("Todo not found", error=True)

    new_name, err = _validate_name(request.form.get("name"))
    if err:
        return render_template("bp/todos/row_edit.html", todo=todo, error=err)

    todo['name'] = new_name
    return render_template("bp/todos/row_display.html", todo=todo) + _toast("Todo updated!")


@bp.route("/<int:todo_id>/toggle", methods=["POST"])
def toggle(todo_id):
    todo = _find_todo(todo_id)
    if not todo:
        return _toast("Todo not found", error=True)

    todo['completed'] = not todo['completed']
    msg = "Marked as done!" if todo['completed'] else "Restored!"
    return render_template("bp/todos/row_display.html", todo=todo) + _toast(msg)


@bp.route("/<int:todo_id>/delete", methods=["POST"])
def delete(todo_id):
    todo = _find_todo(todo_id)
    if not todo:
        return _toast("Todo not found", error=True)

    todos.remove(todo)
    return _toast("Todo deleted!")
