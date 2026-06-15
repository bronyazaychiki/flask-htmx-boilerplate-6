from flask import Blueprint, render_template, request, current_app as app

bp = Blueprint('todos', __name__, url_prefix='/todos')

# In-memory storage (resets on server restart)
todos = [{'id': 1, 'name': 'Clean room'}]
next_id = 2


@bp.route("/", methods=["GET"])
def get_todos():
    """Return the todo list partial (loaded via HTMX on page load)."""
    return render_template("bp/todos/todos.html", todos=todos)


@bp.route("/add", methods=["POST"])
def add_todo():
    """Add a new todo. Returns updated list + toast notification via oob swap."""
    global next_id

    todo_name = request.form.get("todo", "").strip()

    # Validation: empty input
    if not todo_name:
        return render_template(
            "bp/todos/todos.html",
            todos=todos,
            message="请输入任务名称",
            message_type="error",
        )

    # Validation: too long
    if len(todo_name) > 200:
        return render_template(
            "bp/todos/todos.html",
            todos=todos,
            message="任务名称不能超过 200 个字符",
            message_type="error",
        )

    # Add the todo
    todos.append({'id': next_id, 'name': todo_name})
    next_id += 1

    return render_template(
        "bp/todos/todos.html",
        todos=todos,
        message=f"已添加「{todo_name}」",
        message_type="success",
    )


@bp.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    """Delete a todo by ID. Returns updated list + toast notification via oob swap."""
    todo_to_delete = next((t for t in todos if t['id'] == todo_id), None)

    if not todo_to_delete:
        return render_template(
            "bp/todos/todos.html",
            todos=todos,
            message="该任务不存在",
            message_type="error",
        )

    todo_name = todo_to_delete['name']
    todos.remove(todo_to_delete)

    return render_template(
        "bp/todos/todos.html",
        todos=todos,
        message=f"已删除「{todo_name}」",
        message_type="success",
    )
