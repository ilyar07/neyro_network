from flask import Flask, render_template, request
from io import BytesIO
from PIL import Image
import base64
from mymodel import *


app = Flask(__name__)
model = MyModel(train=False)


def show_img(img):
    plt.imshow(img)
    plt.show()


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Главная страница"""

    return render_template('index.html')


@app.route('/detect-int', methods=['POST'])
def detect_int() -> str:
    """Определяет число"""

    data_url = request.form.get('imageBase64').split(',')[1]
    img_bytes = base64.b64decode(data_url)
    img = Image.open(BytesIO(img_bytes))
    img = img.resize((28, 28))
    img = np.array(img)
    img = img[:, :] = img[:, :, 3]
    img = 255 - img
    img = model.convert_image(img)
    result = model.use_model(img)

    return f'{np.argmax(result)},{round(np.max(result) / np.sum(result) * 100, 2)}'
