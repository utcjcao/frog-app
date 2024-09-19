from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import generateSequence
import variables
import trainModel

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

global sequence_number

sequence_number = 0

@socketio.on("generate-sequence") 
def generate_sequence(data):
    global sequence_number

    generated_notes_dict = generateSequence.generate_seeded(data, num_predictions=50)
    socketio.emit('recieve-sequence', generated_notes_dict)
    sequence_number += 1
        

if __name__ == '__main__':
    PORT = 5000  
    socketio.run(app, host='localhost', port=PORT)
