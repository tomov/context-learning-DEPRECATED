from flask import Flask, render_template
import os

# start Flask app
#
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
