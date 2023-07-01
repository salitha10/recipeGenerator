from flask import Flask, render_template, request
from chatgpt import chat
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define route for home page
@app.route("/get", methods=["GET", "POST"])
def gpt_response():
    userText = request.args.get('msg')
    return str(chat(userText))

if __name__ == "__main__":
    app.run(debug=False, port=5005)
