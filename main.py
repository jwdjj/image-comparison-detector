from flask import Flask, render_template
from utilities import compare_images

app = Flask(__name__)

@app.route("/compare")
def compare():
    compare_images()
    main()

@app.route("/")
def main():
    compare_images()
    return render_template('index.html')

if __name__ == "__main__":
    app.run()