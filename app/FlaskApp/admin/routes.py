from flask import Blueprint, request, redirect, render_template, make_response, url_for
from FlaskApp.dbModels import Poll

admin = Blueprint('admin', __name__)

@admin.route('/<int:id>/admin')
def adminView(id):
    '''
        THIS METHOD CHECKS IF THE USER IS ALLOWED TO ACCESS THE ADMIN VIEW,
        AND GENERATES THIS ADMIN VIEW FOR MANAGING THE POLL.
    '''
    poll = Poll.query.get(id)
    if not all([poll, 'authenticated' in request.cookies]):
        return redirect(url_for('poll.pollView', id=id))
    if Poll.check_token(request.cookies['authenticated']) != poll.admin_key:
        return redirect(url_for('poll.pollView', id=id))
    return render_template('admin.html', title=f'Poll #{id} Administation', poll_id=id, is_authenticated=True)

@admin.route('/<int:id>/admin/update', methods=['GET', 'POST'])
def updatePoll(id):
    poll = Poll.query.get(id)  # SELECT THE POLL FROM THE DB BY ITS ID

    # CHECK IF THE USER IS AUTHENTICATED
    if not all([poll, 'authenticated' in request.cookies]): 
        # REDIRECTS THE USER IF NOT AUTHENTICATED
        return redirect(url_for('main.home'))
    
    # CHECKS THE COOKIE AGAINST THE JWT TO MAKE SURE THE USER IS ALLOWED ACCESS
    if Poll.check_token(request.cookies['authenticated']) != poll.admin_key:
        # REDIRECTS THE USER IF NOT AUTHENTICATED
        return redirect(url_for('main.home'))
    
    # CHECKS IF THE POLL IS LIVE, IF SO REDIRECTS THE ADMIN TO THE ADMIN VIEW
    if poll.isLive:
        # REDIRECTS THE USER IF NOT AUTHENTICATED
        return redirect(url_for('admin.adminView', id=id))
    return render_template('update-poll.html', title=f'Poll #{id} Update', is_authenticated=True,  poll_id=id)


@admin.route('/logout')
def logout():
    if 'authenticated' not in request.cookies:
        return redirect(url_for('main.home'))
    next_page = request.args.get('next')
    response = make_response(redirect(url_for('poll.pollView', id=next_page) if next_page else  url_for('main.home')))

    # REMOVES THE AUTHENTICATION COOKIE 
    response.set_cookie('authenticated', '', expires=0)
    return response
