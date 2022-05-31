from flask import render_template
from __init__ import create_app, bd

app=create_app()

@app.route('/')
def index():
    #bd.drop_all()
    #bd.create_all()
    return render_template("index.html")
    if __name__ == '__main__':
        app.run()



