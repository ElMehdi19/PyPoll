from datetime import datetime
from FlaskApp.poll.utils import *
from FlaskApp.poll.forms import newPollForm
from FlaskApp import db
from FlaskApp.dbModels import Poll
from flask import Blueprint, render_template, flash, request, url_for, redirect, make_response


poll = Blueprint('poll', __name__)

@poll.route('/new', methods=['GET', 'POST'])
def newPoll():

    # THIS POLL IS RESPONSIBLE OF RENDRING THE NEWPOLLFORM FOR CREATING POLLS

    form = newPollForm()
    is_authenticated = 'authenticated' in request.cookies
    if form.validate_on_submit():
        # GRABING THE OPTIONS FROM THE FORM DICTIONNARY
        options = [opt for key, opt in request.form.items() if key.startswith('option') ]
        poll_data = {
            'admin_key': secrets.token_hex(16),
            'public_key': secrets.token_hex(8) if 'guests' not in request.form else None,
            'subject': request.form['title'],
            'admin': request.form['email'],
            'options': {key: 0 for key in options},
            'starts': datetime.strptime(request.form['start_date'], '%m/%d/%y %H:%M') if request.form['start_date'] else None,
            'ends': datetime.strptime(request.form['end_date'], '%m/%d/%y %H:%M'),
            'isLive': True if not request.form['start_date'] else False,
            'guestsAllowed': True if 'guests' in request.form else False
        }
        # CREATING A NEW DATABASE INSTANCE AND COMMITING IT 
        # SETTING A COOKIE TO CHECK LATER IF THE ADMIN IS AUTHENTICATED
        # REDIRECTING THE USER TO ADMIN VUE
        new_poll = Poll(public_key=poll_data['public_key'], admin_key=poll_data['admin_key'], 
                        user_email=poll_data['admin'], title=poll_data['subject'], options=poll_data['options'], 
                        start_date=poll_data['starts'], end_date=poll_data['ends'],
                        guestsAllowed=poll_data['guestsAllowed'], isLive=poll_data['isLive']
                        )
        db.session.add(new_poll)
        db.session.commit()
        sendPollData(new_poll.id)
        flash('An email was sent with the poll details.', 'info')
        admin_cookie = new_poll.get_token('admin')
        response = make_response(redirect(url_for('admin.adminView', id=new_poll.id)))
        response.set_cookie('authenticated', admin_cookie)
        return response
    return render_template('new-poll.html', title='New Poll', form=form)

@poll.route('/<int:id>', methods=['GET', 'POST'])
def pollView(id):
    poll = Poll.query.get(id)
    if not poll:
        return redirect(url_for('main.home'))
    if not poll.isLive:
        if poll.start_date <= datetime.utcnow():
            poll.isLive = True
            db.session.commit()
    if poll.end_date <= datetime.utcnow():
        poll.isCompleted = True
        poll.isLive = False
        if not poll.csv_results:
            poll.csv_results = csv_results(poll)
        db.session.commit()
        
    is_authenticated = 'authenticated' in request.cookies
    if is_authenticated and Poll.check_token(request.cookies['authenticated']) == poll.admin_key:
        return redirect(url_for('admin.adminView', id=id))
    return render_template('vote.html', title=f'Poll #{id} vote', poll_id=id, is_authenticated=is_authenticated, 
                            start=poll.start_date, is_live=poll.isLive, is_done=poll.isCompleted, guests=poll.guestsAllowed)
