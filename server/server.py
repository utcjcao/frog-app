from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import generateSequence
import variables
import trainModel

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@socketio("initialize")
def initialize():
    if not variables.get_model_dir().exists():
        socketio.emit('loading')
        trainModel.build_model()
        socketio.emit('done-loading')


@socketio.io("generate-sequence") 
def generate_sequence(data):
    seededSequence = data
    socketio.emit('recieve-sequence', generateSequence.generate_seeded(seededSequence))
        

if __name__ == '__main__':
    PORT = 5000  
    socketio.run(app, host='localhost', port=PORT)
