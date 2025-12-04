from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def view_tasks():
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    search = request.args.get('q', '').strip()

    query = Task.query.filter_by(user_id=current_user.id)

    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)

    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))

    tasks = query.order_by(Task.created_at.desc()).all()

    return render_template(
        'tasks.html',
        tasks=tasks,
        status_filter=status_filter,
        priority_filter=priority_filter,
        search=search
    )


@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'Medium')
    deadline_str = request.form.get('deadline', '').strip()
    time_str = request.form.get('time_slot', '').strip()   # ⭐ FIXED

    if not title:
        flash('Task title cannot be empty.', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    # ---------------------------
    # DEADLINE PARSING
    # ---------------------------
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            flash('Invalid date format for deadline.', 'danger')

    # ---------------------------
    # TIME SLOT PARSING
    # ---------------------------
    time_slot = None
    if time_str:
        try:
            time_slot = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            flash('Invalid time format.', 'danger')

    # ---------------------------
    # CREATE TASK
    # ---------------------------
    task = Task(
        title=title,
        priority=priority,
        deadline=deadline,
        time_slot=time_slot,  # ⭐ WORKS
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Completed'
    else:
        task.status = 'Pending'

    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=['POST'])
@login_required
def clear_tasks():
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All your tasks have been cleared.', 'info')
    return redirect(url_for('tasks.view_tasks'))
