from flask import Flask, render_template, request, redirect, url_for, session, flash
import markdown
import os.path
from os import path
import base64
import hashlib

app = Flask(__name__, template_folder="templates", static_folder=os.path.abspath('../logseq/assets'))

pathPages = "../logseq/pages"


def md_to_html(filename):
    with open(filename, "r") as f:
        md = f.read()
        html = markdown.markdown(md)
        return html


def urlNameToFilename(name: str) -> str:
    absPath = path.abspath(pathPages)
    fullPath = path.join(absPath, name + ".md")
    if path.exists(fullPath):
        return fullPath
    else:
        return ""


def nameToHash(name: str) -> str:
    hasher = hashlib.sha1(name.encode('utf-8'))
    hash = base64.urlsafe_b64encode(hasher.digest()[:5]).decode('utf-8')
    return hash


def getPagesPlusHash(absPath: str) -> list:
    pages = {}
    for page in os.listdir(absPath):
        if page.endswith(".md"):
            pageName = page[:-3]
            pages[pageName] = nameToHash(pageName)
    return pages


@app.route('/', defaults={'name': '', 'key': ''})
@app.route('/<name>/<key>')
def hello_name(name, key):
    print("name: " + name, "key: " + key)
    print(nameToHash(name))
    if name == "":
        return render_template('home.html', pages=getPagesPlusHash(pathPages))
    filename = urlNameToFilename(name)
    if filename == "":
        return render_template('404.html', title="404", description="Not Found"), 404
    else:
        if key == nameToHash(name):
            return render_template('page.html', title=name, content=md_to_html(filename))
        else:
            return render_template('404.html', title="404", description="Unauthorized"), 401


@app.route("/assets/<filename>")
def assets(filename):
    return app.send_static_file(filename)


if __name__ == '__main__':
    app.run(debug=True)
