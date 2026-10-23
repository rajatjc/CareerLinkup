import os

from CareerLinkup import create_app

# initializing flask app
app = create_app()


if __name__ == "__main__":
    # The debugger runs arbitrary code from the browser, so it is opt-in: FLASK_DEBUG=1 python main.py
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=int(os.environ.get("PORT", 5002)))
