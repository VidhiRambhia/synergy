from synergyMain import db, login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True )
    email= db.Column(db.String(120), unique=True, nullable = False)
    password= db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(30), unique=True , nullable= False)
    user_interest1 = db.Column(db.String(40), unique = False , nullable= False )
    user_interest2= db.Column(db.String(40), unique = False , nullable= True )
    user_about = db.Column(db.String(1500), unique= False , nullable= False)
    user_logo = db.Column(db.String(20), unique = False, default = 'default.jpg' , nullable= True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    conversing = db.relationship("Conversing", back_populates ="user")
    def __repr__(self):
        return f"User('{self.user_name}','{self.user_type}','{self.user_interest1}','{self.user_interest2}','{self.user_contactNo1}','{self.user_contactNo2}','{self.user_about}','{self.email}','{self.user_type}''{self.user_logo}')"

class Repository(db.Model):
    __tablename__ = 'repository'
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(20), nullable=False)
    repo_desc = db.Column(db.String(200)) #Description
    #isPublic = db.Column(db.Boolean, nullable=False)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user3 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user4 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)

    def __repr__(self):
        return f"Repository('{self.repo_name}', '{self.repo_desc}')"


class Folder(db.Model):
    __tablename__ = 'folder'
    id = db.Column(db.Integer, primary_key=True)
    repo_id =db.Column(db.Integer, db.ForeignKey('repository.id'), nullable= False)
    folder_filename = db.Column(db.String, default=None, nullable=False)
    folder_url = db.Column(db.String, default=None, nullable=False)

    def __repr__(self):
        return f"File('{self.folder_filename}','{self.folder_url}')"

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    repo_id =db.Column(db.Integer, db.ForeignKey('repository.id'), nullable= False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable= True)
    file_filename = db.Column(db.String, default=None, nullable=False)
    file_url = db.Column(db.String, default=None, nullable=False)

    def __repr__(self):
        return f"File('{self.file_filename}','{self.file_url}')"

'''
class Contributing(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user1 = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=True)
	user = db.relationship("User", back_populates = "contributing")
	user2 = db.Column(db.Integer)
	user3 = db.Column(db.Integer)
	user4 = db.Column(db.Integer)
	history = db.relationship("History", uselist=False, back_populates="contributing")
	request = db.Column(db.Integer)
	status = db.Column(db.String(30), nullable=False, default='none')
	def __repr__(self):
		return f"Contrubuting('{self.user1}', '{self.user2}','{self.user3}', '{self.user4}','{self.request}','{self.status}')"

class History(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	file = db.Column(nullable=False)
	commitMsg = db.Column(db.String(200), nullable=False)
	time = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
	commit_id = db.Column(db.Integer, db.ForeignKey('commit_id'))
	contributing = db.relationship("Contributing", uselist=False, back_populates="history")
	contributor_id = db.Column(db.Integer, nullable=False)
	def __repr__(self):
		return f"History('{self.commitMsg}', '{self.time}','{self.commit_id}','{self.contributor_id}','{self.file}')"
'''
class Conversing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user = db.relationship("User", back_populates ="conversing")
    user2 = db.Column(db.Integer)
    conversation=db.relationship("Conversation", uselist=False, back_populates ="conversing")
    request = db.Column(db.Integer)
    status = db.Column(db.String(30), nullable=False, default= 'none')
    def __repr__(self):
        return f"Conversing('{self.user1}','{self.user2}','{self.request}','{self.status}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    conversing_id = db.Column(db.Integer, db.ForeignKey('conversing.id'))
    conversing= db.relationship("Conversing", uselist=False, back_populates ="conversation" )
    sender_id = db.Column(db.Integer, unique = False , nullable= False )
    def __repr__(self):
        return f"Conversation('{self.text}','{self.time}','{self.conversing_id}', '{self.sender_id}')"

