import os
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta

# Create a simple Flask app
app = Flask(__name__)

# In-memory database for tasks (will reset on server restart)
tasks = []

@app.route('/')
def index():
    """Render the main to-do list page with date-based sections"""
    # Calculate dates for filtering
    today = datetime.now().date()
    today_str = today.strftime('%d-%m-%Y')
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%d-%m-%Y')
    next_week = today + timedelta(days=7)
    next_week_str = next_week.strftime('%d-%m-%Y')
    
    return render_template(
        'index.html', 
        tasks=tasks,
        today_date=today_str,
        tomorrow_date=tomorrow_str,
        next_week_date=next_week_str
    )

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    
    if title:
        # Create a new task with a simple ID
        task_id = len(tasks) + 1
        new_task = {
            'id': task_id,
            'title': title,
            'due_date': datetime.strptime(due_date, '%Y-%m-%d').strftime('%d-%m-%Y') if due_date else 'No due date',
            'category': request.form.get('category') or 'General',  # Add category field
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(new_task)
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    
    return redirect(url_for('index'))

# This makes the app work with Gunicorn
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
