from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from tkinter import filedialog
from PIL import Image
import numpy as np
import os
from datetime import date
from werkzeug.utils import secure_filename

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "static/images/"

bootstrap = Bootstrap(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    # Current year, copyright
    current_year = date.today().year

    if request.method == 'POST':
        histogram = {}

        default_value = '10'
        n_colours = request.form.get('n_colours') or default_value

        # Open file explorer and get image path
        # tkinter, part of Tk widget toolkit is not compatible with Heroku
        # filename = filedialog.askopenfile(initialdir='/', title="Select image",
        #                                   filetypes=(("Image files", '*.png*'), ("Image files", "*.jpg*")))

        file = request.files['file']

        # Get secure version of filename, i.e. replace spaces with underline...
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file_path = f"static/images/{file.filename}"

        # file_path = filename.name

        img = Image.open(file_path)
        # PIL image to numpy array, 3rd dimension remove 4th element
        imgarray = np.array(img)[:, :, :3]

        # Arrange all pixels into a tall column of 3 RGB values and find unique rows (colours)
        colours, counts = np.unique(imgarray.reshape(-1, 3), axis=0, return_counts=1)

        colours_list = colours.tolist()
        counts_list = counts.tolist()

        # Sort colours list based on counts list
        result_list = [i for _, i in sorted(zip(counts_list, colours_list))]

        # Take last N colours
        result_f = result_list[-int(n_colours):]

        # Reformat to hex values
        hex_colours = []
        for colour in result_f:
            hex_v = '#%02x%02x%02x' % (colour[0], colour[1], colour[2])
            hex_colours.append(hex_v)
        print(hex_colours)

        return render_template("index.html", number=int(n_colours), colours=hex_colours, year=current_year)

    return render_template("index.html", year=current_year)


if __name__ == '__main__':
    app.run(debug=True)
