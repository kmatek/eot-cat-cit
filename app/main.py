from flaskr import create_app

app = create_app()

if __name__ == '__main__':
    # Run the application with host, port and debug from app config
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'])
