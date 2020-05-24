from flask import current_app
from FlaskApp import db
from datetime import datetime
from itsdangerous import JSONWebSignatureSerializer as serializer

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(8), default=None)
    admin_key = db.Column(db.String(16), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    title = db.Column(db.Text, nullable=False)
    options = db.Column(db.PickleType, nullable=False, default={})
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    isLive = db.Column(db.Boolean, nullable=False, default=False)
    isCompleted = db.Column(db.Boolean, nullable=False, default=False)
    votes = db.Column(db.Integer, default=0)
    csv_results = db.Column(db.String(35))
    guestsAllowed = db.Column(db.Boolean, default=False)

    '''
        This method generates a JSON web token which will be used to authenticate API access.
    '''
    def get_token(self, reason):
        s = serializer(current_app.secret_key)
        if reason == 'admin':
            return s.dumps({'KEY': self.admin_key}).decode('UTF-8')
        return s.dumps({'KEY': self.public_key}).decode('UTF-8')
    
    '''
        This method checks wheter a JSON web token is valid, 
        and if so the user with this JWT will be granted access to the API.
    '''
    @staticmethod
    def check_token(token):
        s = serializer(current_app.secret_key)
        try:
            valid = s.loads(token)
        except Exception:
            return False
        return valid['KEY']
    def __repr__(self):
        return f"Poll({self.id, self.title, self.isLive})"
