import os
import secrets
from synergyMain import app, db
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from synergyMain.forms import LoginForm, SelectForm, UpdateAccountForm
from synergyMain.models import User, Conversing, Conversation
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
from math import sqrt
import requests
from geopy.geocoders import Nominatim
from sqlalchemy import or_ , and_
from flask import send_from_directory

UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    form= SelectForm(request.form)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
            if form.validate_on_submit():
                pw = (form.password.data)
                s = 0
                for char in pw:
                   a = ord(char) #ASCII
                   s = s+a #sum of ASCIIs acts as the salt
                hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
                user = User(email=form.email.data, password=hashed_password,user_name=form.user_name,user_interest1 = form.user_interest1,user_interest2 = form.user_interest2, user_about= form.user_about)
                
                if form.user_logo.data:
                    picture_file = save_picture(form.user_logo.data)
                    user.user_logo = picture_file

                db.session.add(user)
                db.session.commit()
                flash(f'Success! Please login and start developing', 'success')
                user_logo = url_for('static', filename='profile_pics/' + user.user_logo)
            return redirect(url_for('login'))
    else: print('halaaaa')
    return render_template('reg.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #modified to use SHA512

        s = 0
        for char in (form.password.data):
            a = ord(char)
            s = s+a
        now_hash = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if (user and (user.password==now_hash)):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))

        else:
            print('swallalala')
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print('shimmy shimmy')
    else:
        print('swallalala')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods= ['POST', 'GET'])
@login_required
def account():
 
    form = UpdateAccountForm()
    user==User.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.user_logo = picture_file
        current_user.email = form.email.data
        user.user_name=form.sponsor_name.data
        user.user_about=form.sponsor_about.data
        user.user_interest1=form.user_interest1.data
        user.user_interest2=form.user_interest2.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.user_name.data=user.user_name
        form.user_about.data=user.user_about
        form.user_interest1.data=user.user_interest1
        form.user_interest2.data=user.user_interest2
            
    user_logo = url_for('static', filename='profile_pics/' + user.user_logo)
    return render_template('account.html', title='Account',user_logo = user_logo, form=form)


@app.route("/shortlist/<user2_id>", methods= ['POST', 'GET'])
@login_required
def shortlisted(user2_id):

    form = InviteForm()

    if current_user.type == 'S':
        shortlisted_user=user.query.filter_by(user_id=user2_id).first()

        flag=0
        for user in shortlist:
            if user.user_id == shortlisted_user.user_id:
                flag=1
                print("nahin hua")
                break
        if flag==0:
            shortlist.append(shortlisted_user)
            print("hua")

        print(shortlist)
        #session.expunge(shortlisted_user)
        db.session.commit()
        return render_template ('shortlistPageSponsor.html', title = 'Shortlist', userList=shortlist, form=form)


    elif current_user.type =='P':
        shortlisted_user=SponsorUser.query.filter_by(user_id=user2_id).first()

        flag=0
        for sponsorUser in shortlist:
            if sponsorUser.user_id == shortlisted_user.user_id:
                flag=1
                print("nahin hua")
                break
        if flag==0:
            shortlist.append(shortlisted_user)
            print("hua")

        print(shortlist)
        #session.expunge(shortlisted_user)
        db.session.commit()
        return render_template ('shortlistPageuser.html', title = 'Shortlist', userList=shortlist, form=form)



@app.route("/display_shortlist", methods = ['GET','POST'])
@login_required
def display_shortlist():

    form = InviteForm()

    if current_user.type == 'S':
        return render_template ('shortlistPageSponsor.html', title = 'Shortlist', userList=shortlist, form=form)

    elif current_user.type == 'P':
        return render_template ('shortlistPageuser.html', title = 'Shortlist', userList=shortlist, form=form)



@app.route("/chatwith", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chatwith():
    associated_users_list=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).all()
    conversing2= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).first()


    if conversing2 == None:
        print('10001')
        return render_template ('chatError.html', title = 'Chat Error',current_user=current_user)
    else:
        for nowuser in conversing :
            print('1000')
            print(nowuser.status)
            if nowuser.user1== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        user= user.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[user.user_id,user.user_name]
                        associated_users_list.append(associated_user)
            elif nowuser.user2== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        user= user.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[user.user_id,user.user_name]
                        associated_users_list.append(associated_user)
        if associated_users_list==[]:
            return render_template ('chatError.html', title = 'No Users')
        return render_template ('chatlist.html', title = 'Chat with', associated_users_list=associated_users_list)



    #return associated_users_choices
@app.route("/chatbox/<chatwith_id>", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chat(chatwith_id):
    print(chatwith_id)
    form=ChatBoxText()
    messages=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==chatwith_id,Conversing.user2==chatwith_id)).all()
    for nowuser in conversing:
        if current_user.type=='P':
            if nowuser.user1== current_user.id:

                user=SponsorUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

            elif  nowuser.user2==current_user.id:
                user=SponsorUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]#just for now
                    messages.append(message)

        elif current_user.type=='S':
            if nowuser.user1== current_user.id :
                user=user.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.user_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

            elif nowuser.user2==current_user.id :
                user=user.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.user_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                        #user=user.query.filter_by(user_id=chatwith_id).first()#just for now
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

    return render_template('chatbox.html', title= 'ChatBox', form=form, messages=messages, current_user=current_user, user=user)




@app.route("/filterType/<type>", methods = ['GET', 'POST'])
@login_required
def filterType(type):

    if current_user.type == 'P':

        user = user.query.filter_by(user_id= current_user.id).first()

        lat = user.user_latitude
        lng = user.user_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_type=type).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements, user = user)

    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyuserFunc()
        filteredList = user.query.filter_by(user_type=type).all()
        filteredParties = []

        for user in filteredList:
            user_data = [user.user_name, user.user_latitude, user.user_longitude, user.user_address, user.user_id]
            filteredParties.append(user_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements, sponsorUser = sponsorUser)




@app.route("/filterKind/<kind>", methods = ['GET', 'POST'])
@login_required
def filterKind(kind):

    if current_user.type == 'P':

        user = user.query.filter_by(user_id= current_user.id).first()

        lat = user.user_latitude
        lng = user.user_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_kind=kind).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements, user = user)


    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyuserFunc()
        filteredList = user.query.filter_by(user_kind=kind).all()
        filteredParties = []

        for user in filteredList:
            user_data = [user.user_name, user.user_latitude, user.user_longitude, user.user_address, user.user_id]
            filteredParties.append(user_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements, sponsorUser = sponsorUser)


def allowed_file(filename):
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return '.' in filename and '/'


@app.route("/uploads", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("swallalala")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            print(filename);
            file_path = os.path.join(app.root_path, 'UPLOAD_FOLDER/', filename)
            #file.save(os.path.join('UPLOAD_FOLDER'))
            file.save(file_path)
    return render_template('uploads.html', title='Upload')
    

@app.route('/uploads/<filename>')
def view_uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/MeetTheTeam")
def team():
    return render_template('MeetTheTeam.html')

@app.route("/WhatWeDo")
def work():
    return render_template('WhatWeDo.html')
