import io

from base64 import b64encode
from flask import Flask, send_file, render_template, request
from flask_mail import Mail, Message

from filters.CartoonFilter import Cartoonizer
from filters.CoolFilter import Cool
from filters.NegativeFilter import Negative
from filters.VintageFilter import Vintage

app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)

negative = Negative()
cartoon = Cartoonizer()
vintage = Vintage()
cool = Cool()


@app.route('/sendEmail', methods=["POST"])
def send_email():
    result_bytes = process_filter()
    if not result_bytes:
        return render_template('init.html', image=None, alert='Вставьте изображение')
    email = request.form['email']
    if not email:
        return render_template('init.html', image=None, alert='Введите почту')
    msg = Message("Filter photo", recipients=[email])
    msg.body = "Обработанное изображение:"
    msg.attach("image.jpg", "image/jpg", result_bytes)
    mail.send(msg)
    return render_template('init.html', image=None, alert='Изображение отправлено')


@app.route('/')
def init():
    return render_template("init.html", image=None, alert=None)


@app.route('/', methods=['POST'])
def post_init():
    alert = request.form['alert']
    return render_template("init.html", image=None, alert=alert)


@app.route('/filterPhoto', methods=['POST'])
def filter_photo():
    result_bytes = process_filter()
    if not result_bytes:
        return render_template('init.html', image=None, alert='Вставьте изображение')
    image = b64encode(result_bytes).decode("utf-8")
    return render_template("init.html", image=image, alert=None)


@app.route('/downloadPhoto', methods=['POST'])
def download_photo():
    result_bytes = process_filter()
    if not result_bytes:
        return render_template('init.html', image=None, alert='Вставьте изображение')
    mem = io.BytesIO()
    mem.write(result_bytes)
    mem.seek(0)
    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='image.jpg',
        mimetype='image/jpeg'
    )


def process_filter():
    file = request.files['file']
    if not file:
        return None

    photo = file.read()
    filterType = request.form['filters']
    if filterType == 'negative':
        resultBytes = negativeFilter(photo)
    elif filterType == 'cartoon':
        resultBytes = cartoonFilter(photo)
    elif filterType == 'vintage':
        resultBytes = vintageFilter(photo)
    elif filterType == 'cool':
        resultBytes = coolFilter(photo)
    else:
        resultBytes = negativeFilter(photo)
    return resultBytes


def negativeFilter(f):
    return negative.render(f)


def cartoonFilter(f):
    return cartoon.render(f)


def vintageFilter(f):
    return vintage.render(f)


def coolFilter(f):
    return cool.render(f)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
