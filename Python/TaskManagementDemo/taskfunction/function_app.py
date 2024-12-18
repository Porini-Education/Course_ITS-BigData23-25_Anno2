import azure.functions as func
import logging
import pyodbc
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def _get_connection():
    sql_server_connection_string = os.getenv("sql_server_connection_string")
    if not sql_server_connection_string:
        logging.error("Please set the 'sql_server_connection_string' environment variable")
        return None, func.HttpResponse(
            "Please set the 'sql_server_connection_string' environment variable", status_code=500
        )
    return pyodbc.connect(f'{sql_server_connection_string}'), None

@app.route(route="add_task")
def add_task(req: func.HttpRequest) -> func.HttpResponse:    
    task = {}
    try:
        req_body = req.get_json()
        task['taskName'] = req_body.get('task')
        task['category'] = req_body.get('category')
        task['priority'] = req_body.get('priority')
    except ValueError:
        pass

    if task and task['taskName']:
        conn, error = _get_connection()
        if not conn:
            return error or func.HttpResponse("Unknown error", status_code=500)

        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO dbo.Tasks (Task, Category, Priority, Status) VALUES (?, ?, ?, 'Pending')", task['taskName'], task['category'], task['priority'])

        except Exception as e:
            logging.error(f"Error inserting task: {str(e)}")
            return func.HttpResponse(
                f"Error inserting task: {str(e)}", status_code=500
            )

        return func.HttpResponse(
            f"Task '{task}' added successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Please pass a task in the request body", status_code=400
        )

@app.route(route="get_tasks", auth_level=func.AuthLevel.FUNCTION)
def get_tasks(req: func.HttpRequest) -> func.HttpResponse:
    conn, error = _get_connection()
    if not conn:
        return error or func.HttpResponse("Unknown error", status_code=500)

    tasks_list = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Id, Task, Category, Priority, Status FROM dbo.Tasks")
            tasks = cursor.fetchall()
            tasks_list = [{'id': row[0], 'task': row[1], 'category': row[2], 'priority': row[3], 'status': row[4]} for row in tasks]
    except Exception as e:
        logging.error(f"Error reading tasks: {str(e)}")
        return func.HttpResponse(
            f"Error reading tasks: {str(e)}", status_code=500
        )
    return func.HttpResponse(json.dumps({'tasks': tasks_list}), status_code=200)


@app.route(route="update_task", auth_level=func.AuthLevel.FUNCTION)
def update_task(req: func.HttpRequest) -> func.HttpResponse:
    task_id = req.get_json().get('id')
    new_status = req.get_json().get('status')
    if not task_id or not new_status:
        return func.HttpResponse("Please provide a task id and a new status", status_code=400)
    
    conn, error = _get_connection()
    if not conn:
        return error or func.HttpResponse("Unknown error", status_code=500)
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE Tasks SET Status = ? WHERE Id = ?", new_status, task_id)
            conn.commit()
    except Exception as e:
        logging.error(f"Error updating task: {str(e)}")
        return func.HttpResponse(
            f"Error updating task: {str(e)}", status_code=500
        )
    
    return func.HttpResponse(json.dumps({'status': 'Task updated', 'id': task_id, 'new_status': new_status}), status_code=200)