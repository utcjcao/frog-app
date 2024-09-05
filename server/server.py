from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import generateSequence
import variables
import trainModel

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

sequence_number = 0

@socketio.on("generate-sequence") 
def generate_sequence(data):
    seededSequence = data
    generateSequence.generate_seeded(seededSequence, sequence_number=sequence_number)
    socketio.emit('recieve-sequence', sequence_number)
    sequence_number += 1
        

if __name__ == '__main__':
    PORT = 5000  
    socketio.run(app, host='localhost', port=PORT)
