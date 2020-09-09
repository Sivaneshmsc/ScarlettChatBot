import flask
import aiml
import os
from waitress import serve

app = flask.Flask(__name__)
app.config["DEBUG"] = True

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles=os.path.abspath("brain.aiml"), commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")

@app.route('/', methods=['POST'])
def home():
    data = flask.request.get_json()
    bot_response = kernel.respond(data)
    return bot_response

serve(app, host='localhost', port=8877)
