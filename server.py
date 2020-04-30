import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from flask_cors import CORS

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
MAX_ALLOWED_SESSION_DURATION = 14400

app = Flask(__name__)
CORS(app)


def generateToken():
    return AccessToken(twilio_account_sid, twilio_api_key_sid, twilio_api_key_secret)


def videoToken(identity, room):
    videoGrant = None
    if not room == None:
        videoGrant = VideoGrant(room=room)
    else:
        videoGrant = VideoGrant()
    token = generateToken()
    token.add_grant(videoGrant)
    token.identity = identity
    return token


@app.route('/token', methods=['GET'])
def getVideoToken():
    identity = request.args.get("identity")
    roomName = request.args.get("roomName")
    print(identity)
    print(roomName)
    token = videoToken(identity, roomName)
    return token.to_jwt().decode()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3005)
