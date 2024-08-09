from website import db,login_manager
from website import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email_id = db.Column(db.String(50),nullable=False,unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    @property
    def password(self):
        return self.password 
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email_id = db.Column(db.String(50),nullable=False,unique=True)
    industry = db.Column(db.String(100))
    budget = db.Column(db.Float)

    user = db.relationship('User', backref=db.backref('sponsor', lazy=True))

    def __repr__(self):
        return f"<Sponsor {self.name}>"

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email_id = db.Column(db.String(50),nullable =False,unique =True)
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('influencer', lazy=True))

    def __repr__(self):
        return f"<Influencer {self.name}>"

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    status = db.Column(db.String(20),nullable=False)
    visibility = db.Column(db.String(50), nullable=False)
    goals = db.Column(db.Text)

    sponsor = db.relationship('Sponsor', backref=db.backref('campaigns', lazy=True))

    def __repr__(self):
        return f"<Campaign {self.name}>"

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(50), nullable=False)

    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', lazy=True))
    influencer = db.relationship('Influencer', backref=db.backref('ad_requests', lazy=True))

    def __repr__(self):
        return f"<AdRequest {self.id}>"

class AdminFlag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    reason = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('flags', lazy=True))
    campaign = db.relationship('Campaign', backref=db.backref('flags', lazy=True))

    def __repr__(self):
        return f"<AdminFlag {self.id}>"
