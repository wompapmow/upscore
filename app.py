from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from os import urandom

import score

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(32)

class ScoreInput(FlaskForm):
    before = TextAreaField('Before', render_kw={"rows": 25, "cols": 80})
    after = TextAreaField('After', render_kw={"rows": 25, "cols": 80})
    submit = SubmitField("Can I call you a dancing master?")

class ScoreOutput(object):
    pass

@app.route('/', methods=['GET', 'POST'])
def input(songs=None):
    form = ScoreInput()
    if request.method == 'POST':
        songs = score.output(request.form['before'], request.form['after'])
        print(songs)
        # return redirect(url_for('score_output', songs))
        return render_template('scores.html', songs=songs)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(port=8080)
