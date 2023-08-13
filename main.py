from CareerLinkup import create_app

# initializing flask app
app = create_app()


if __name__ == "__main__":
    app.run(debug=True,port=5002)
   