from website import create_app

app = create_app()

if __name__ == '__main__': # only if run file will we execute
    app.run(debug=True) # run flask app and web server - will rerun webserver for changes
