import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
from flask import Blueprint, redirect, url_for, session, request, flash
from flask_login import login_required, current_user
from google_auth_oauthlib.flow import Flow
from datetime import datetime


from app.extensions import db

google_bp = Blueprint('google', __name__, url_prefix='/google')

# OAuth configuration
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

print("DEBUG GOOGLE CLIENT ID =", CLIENT_ID)
# -------------------------------------------------
# CONNECT GOOGLE CALENDAR
# -------------------------------------------------
@google_bp.route('/connect')
@login_required
def connect_google():
    if not CLIENT_ID or not CLIENT_SECRET:
        flash("Google OAuth credentials not configured.", "danger")
        return redirect(url_for('tasks.view_tasks'))

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=url_for('google.google_callback', _external=True)
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    session['oauth_state'] = state
    return redirect(authorization_url)


# -------------------------------------------------
# GOOGLE OAUTH CALLBACK
# -------------------------------------------------
@google_bp.route('/callback')
@login_required
def google_callback():
    state = session.get('oauth_state')

    if not state:
        flash("OAuth session expired. Try again.", "danger")
        return redirect(url_for('tasks.view_tasks'))

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('google.google_callback', _external=True)
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Store tokens in DB (CRITICAL)
    current_user.google_access_token = credentials.token
    current_user.google_refresh_token = credentials.refresh_token
    current_user.google_token_expiry = credentials.expiry

    db.session.commit()

    flash("Google Calendar connected successfully!", "success")
    return redirect(url_for('tasks.view_tasks'))
