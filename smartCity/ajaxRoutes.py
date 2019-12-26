from smartCity import app
from flask import render_template, url_for, flash, redirect, request, jsonify

@app.route("/findName")
def test():
    name = str(request.args.get('name'))
    age = str(request.args.get('age'))
    return jsonify({
        'name' : name,
        'age' : age
        })

