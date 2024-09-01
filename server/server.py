from flask import Flask,
from flask_socketio import SocketIO
import generateSequence
import variables
import trainModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio("initialize")
def initialize():
    if not variables.get_model_dir().exists():
        socketio.emit('loading')
        trainModel.build_model()
        

@socketio.io("generate-sequence") 
def generate_sequence(data):
    sequenceType, seededSequence = data
    if sequenceType == "random":
        generateSequence.generate_random()
    elif sequenceType == "seeded":
        generateSequence.generate_seeded(seededSequence)


socketio.run(app)