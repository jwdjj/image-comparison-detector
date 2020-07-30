from flask import Flask, render_template, redirect, send_file
from utilities import compare_images

app = Flask(__name__)

# On generate default database comparison click
@app.route("/compare")
def compare():
    compare_images()

    # to return saved comparison result .csv
    return send_file('output.csv',
                     mimetype='text/csv',
                     attachment_filename='result.csv',
                     as_attachment=True)

# Main page - index.html
@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()