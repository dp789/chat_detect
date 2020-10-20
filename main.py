import requests
from flask import Flask, request, make_response, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    token = db.Column(db.String(250))
    ip = db.Column(db.String(250))


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(250))
    from_username = db.Column(db.String(250))
    to_user = db.Column(db.String(250))
    to_username = db.Column(db.String(250))
    message = db.Column(db.Text)


@app.route('/set-token', methods=['POST'])
def set_token():
    data = request.get_json()
    username = data['username']
    token = data['token']
    ip = data['ip']
    user_token = UserToken.query.filter_by(username=username).scalar()

    if user_token:
        user_token.token = token
        user_token.ip = ip
    else:
        new_user_token = UserToken(username=username, token=token, ip=ip)
        db.session.add(new_user_token)

    db.session.commit()

    return make_response(jsonify({'message': 'User token set'})), 200


@app.route('/send', methods=['POST'])
def get_token():
    data = request.get_json()
    from_ip = data['ip']
    to_username = data['toUsername']
    from_username = data['fromUsername']
    message = data['message']
    to_user = UserToken.query.filter_by(username=to_username).scalar()

    if to_user:
        to_ip = to_user.ip
        new_message = Messages(from_user=from_ip, to_user=to_ip, from_username=from_username, to_username=to_username,
                               message=message)
        db.session.add(new_message)
        db.session.commit()
    else:
        return make_response(jsonify({"message": "No user exists with the given username"})), 400

    # token = "dVwu4oW2gcM:APA91bEizQVhsHqZoUeIoO5pIBeUz-x_56xAdk37_jOv1MnlHJfL672LRs7pi_2D5dJEvcIDi2FH8OSvZCrfFz_ML1mjb0-AfQihQq3iOpDVqukfycNqwy57Hw0IzUXDiGXBL_uCBNPj"
    token = to_user.token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "key=AAAA6Fzt-wc:APA91bHuZB6h_8jG-5LCoy5bzchwlZ9XgEmSGL8NhpF1Uw5VOiaceL2RpBLE-oXRc2itf4QwNU2lcJZNdNeJg45hnw2ATOE648fSDSUR0F-7OhJG6gy9c9TnrKwDnmPQhhM3HLFbkpgf"
    }
    payload = {
        'to': token,
        'data': {
            'message': message,
            'from_email': from_username
        }
    }

    result = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(payload))

    if result.status_code == 200:
        print("Message sent")

        return make_response(jsonify({'message': 'Message sent'})), 200
    else:
        return make_response(jsonify({'message': 'Could not send message'})), 400


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, use_reloader=False)
