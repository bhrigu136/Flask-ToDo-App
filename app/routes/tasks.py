# Flask-ToDo_App\app\routes\tasks.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, time
from app.extensions import db
from app.models import Task

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import timedelta
import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


tasks_bp = Blueprint('tasks', __name__)


# VIEW TASKS
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



# ADD TASK

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'Medium')
    deadline_str = request.form.get('deadline', '').strip()
    time_str = request.form.get('time_slot', '').strip()

    if not title:
        flash('Task title cannot be empty.', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    
    # DEADLINE PARSING (DATE)
    
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            flash('Invalid date format for deadline.', 'danger')
            return redirect(url_for('tasks.view_tasks'))

    
    # TIME SLOT PARSING (TIME)
    
    time_slot = None
    if time_str:
        try:
            time_slot = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            flash('Invalid time format.', 'danger')
            return redirect(url_for('tasks.view_tasks'))

    
    # COMBINE DATE + TIME
    
    deadline_datetime = None
    if deadline and time_slot:
        deadline_datetime = datetime.combine(deadline, time_slot)
    elif deadline:
        # Default reminder time if user gives only date
        deadline_datetime = datetime.combine(deadline, time(9, 0))

    # (IMPORTANT)
    # We are NOT storing deadline_datetime yet.
    # This will be used for Google Calendar in next step.

    
    # CREATE TASK
    
    task = Task(
        title=title,
        priority=priority,
        deadline=deadline,
        time_slot=time_slot,
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    # CREATE GOOGLE CALENDAR EVENT (IF CONNECTED)
    if (
        deadline_datetime
        and current_user.google_access_token
        and current_user.google_refresh_token
    ):
        try:
            creds = Credentials(
                token=current_user.google_access_token,
                refresh_token=current_user.google_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
            )

            service = build("calendar", "v3", credentials=creds)

            event = {
                "summary": f"To-Do: {task.title}",
                "description": f"Priority: {task.priority}",
                "start": {
                    "dateTime": deadline_datetime.isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": (deadline_datetime + timedelta(minutes=30)).isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 60},
                        {"method": "popup", "minutes": 10},
                    ],
                },
            }

            created_event = service.events().insert(
                calendarId="primary",
                body=event
            ).execute()

            task.google_event_id = created_event.get("id")
            db.session.commit()

        except Exception as e:
            # Do NOT crash app for calendar failures
            print("Google Calendar error:", e)

    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks.view_tasks'))


# EDIT TASK
@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'Medium')
    deadline_str = request.form.get('deadline', '').strip()
    time_str = request.form.get('time_slot', '').strip()

    if not title:
        flash("Task title cannot be empty.", "danger")
        return redirect(url_for('tasks.view_tasks'))

    
    # PARSE DATE
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for('tasks.view_tasks'))

    # PARSE TIME    
    time_slot = None
    if time_str:
        try:
            time_slot = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            flash("Invalid time format.", "danger")
            return redirect(url_for('tasks.view_tasks'))

  
    # UPDATE TASK
    
    task.title = title
    task.priority = priority
    task.deadline = deadline
    task.time_slot = time_slot

    db.session.commit()

    # UPDATE GOOGLE CALENDAR EVENT (IF EXISTS)
    if (
        task.google_event_id
        and current_user.google_access_token
        and current_user.google_refresh_token
        and (deadline or time_slot)
    ):
        try:
            # Rebuild datetime
            deadline_datetime = None
            if deadline and time_slot:
                deadline_datetime = datetime.combine(deadline, time_slot)
            elif deadline:
                deadline_datetime = datetime.combine(deadline, time(9, 0))

            if deadline_datetime:
                creds = Credentials(
                    token=current_user.google_access_token,
                    refresh_token=current_user.google_refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=GOOGLE_CLIENT_ID,
                    client_secret=GOOGLE_CLIENT_SECRET,
                )

                service = build("calendar", "v3", credentials=creds)

                updated_event = {
                    "summary": f"To-Do: {task.title}",
                    "description": f"Priority: {task.priority}",
                    "start": {
                        "dateTime": deadline_datetime.isoformat(),
                        "timeZone": "Asia/Kolkata",
                    },
                    "end": {
                        "dateTime": (deadline_datetime + timedelta(minutes=30)).isoformat(),
                        "timeZone": "Asia/Kolkata",
                    },
                }

                service.events().patch(
                    calendarId="primary",
                    eventId=task.google_event_id,
                    body=updated_event
                ).execute()

        except Exception as e:
            # Never block user edit for Google failures
            print("Google Calendar update failed:", e)

    flash("Task updated successfully.", "success")
    return redirect(url_for('tasks.view_tasks'))



# TOGGLE TASK STATUS
@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Completed'
    else:
        task.status = 'Pending'

    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


# DELETE TASK

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    
    # DELETE GOOGLE CALENDAR EVENT (IF EXISTS)

    if (
        task.google_event_id
        and current_user.google_access_token
        and current_user.google_refresh_token
    ):
        try:
            creds = Credentials(
                token=current_user.google_access_token,
                refresh_token=current_user.google_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
            )

            service = build("calendar", "v3", credentials=creds)

            service.events().delete(
                calendarId="primary",
                eventId=task.google_event_id
            ).execute()

        except Exception as e:
            # Never block deletion if Google fails
            print("Google Calendar delete failed:", e)

    
    # DELETE LOCAL TASK
    
    db.session.delete(task)
    db.session.commit()

    flash('Task deleted.', 'info')
    return redirect(url_for('tasks.view_tasks'))



# CLEAR ALL TASKS

@tasks_bp.route('/clear', methods=['POST'])
@login_required
def clear_tasks():
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All your tasks have been cleared.', 'info')
    return redirect(url_for('tasks.view_tasks'))
