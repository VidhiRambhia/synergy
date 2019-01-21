import os
import secrets
from synergy import app, db
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from synergy.forms import RegistrationForm, LoginForm, SelectForm,UpdateAccountForm, ChatBoxText, RequestForm, InviteForm
from synergy.models import PartyUser, SponsorUser, User, Conversing, Conversation
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
from sqlalchemy import or_ , and_

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')