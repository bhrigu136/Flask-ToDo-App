from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # local only; Render uses gunicorn
