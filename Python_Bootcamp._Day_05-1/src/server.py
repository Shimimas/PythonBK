import flask
import os
import werkzeug.utils
from bs4 import BeautifulSoup

app = flask.Flask(__name__)

UPLOAD_FOLDER = 'server'
ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

use_set = set()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    with open('page.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        if file and allowed_file(file.filename):
            if file.filename not in use_set:
                use_set.add(file.filename)
                new_tag = soup.new_tag("h")
                soup.append(new_tag)
                soup.find_all('h')[-1].string = f"{file.filename}"
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open("page.html", "w") as file_write:
                file_write.write(soup.prettify())
            return flask.redirect(flask.url_for('upload_file', name=filename))
        else:
            return "Non-audio file detected"
    return soup.prettify()

if __name__ == "__main__":
    app.run('localhost', 8888)