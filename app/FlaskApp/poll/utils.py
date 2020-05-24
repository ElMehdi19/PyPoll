import os, secrets, csv
from FlaskApp import mail
from flask import url_for, current_app
from flask_mail import Message
from FlaskApp.dbModels import Poll

def sendPollData(poll_id):

    # SENDING AN EMAIL UPON POLL CREATION WHICH INCLUDES INFORMATION ABOUT THE POLL

    poll = Poll.query.get(poll_id)
    msg = Message('Your poll was created!', sender='noreply@demo.com', recipients=[poll.user_email])
    msg.html = f"""Your new poll has been created successfully!<br>
<b>Details:</b>
<ul>
    <li>Voting link: { url_for('poll.pollView', id=poll.id, _external=True) }</li>
    <li>Admin Key: <b>{ poll.admin_key }</b></li>
    <li>Public Key: <b>{ poll.public_key }</b></li>
</ul>
<h3>Don't forget to share the voting link (and the public key if guests aren't allowed) so people can vote.</h3><br><br>
<h4>See you soon<br><b>PyPoll<b></h4>
    """
    mail.send(msg)


def csv_results(poll):

    # EXPORTING THE POLL RESULTS TO CSV FILE

    fields = ['title', 'votes', 'options', 'results', 'start_date', 'end_date', 'timespan']
    token = secrets.token_hex(8)
    csv_name = f'poll_results_{poll.id}_{token}.csv'
    csv_path = os.path.join(current_app.root_path, 'static/csv', csv_name)

    with open(csv_path, 'w', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fields)
        csv_writer.writeheader()
        options = poll.options
        options = {key:options[key] for key in sorted(options.keys(), key=poll.options.get)}
        data = {'title':poll.title, 'votes':poll.votes, 
                'options':list(options.keys()), 'results':list(options.values()), 
                'start_date':poll.start_date, 'end_date':poll.end_date, 
                'timespan': poll.end_date - poll.start_date
                }
        csv_writer.writerow(data)
    return csv_name

# IN CASE YOU WANT TO VISUALISE THE RESULTS USING PYTHON INSTEAD OF ChartJS
# def display_results(poll):
    # options = poll.options
    # results = { key:options[key] for key in sorted(options, key=options.get)}
    # # DON'T FORGET TO INSTALL matplotlib AND TO IMPORT pyplot FROM IT AS plt !!
    # with plt.style.context('fivethirtyeight'):
    #     x_axis = list(results.values())
    #     y_axis = list(results.keys())
    #     if len(options) <= 4:
    #         fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    #         ax1.set_title('Pie Chart')
    #         ax2.set_title('Bar Chart')
    #         ax1.pie(x_axis, explode=[0.01 for _ in range(len(x_axis))], labels=y_axis,
    #                 autopct=lambda p: f'{p:.2f}%', radius=1.5)
    #         ax2.barh(y_axis, x_axis, height=0.2)
    #         fig.tight_layout()
    #     else:
    #         plt.title('Poll results as bar chart')
    #         plt.xlabel('Number of votes')
    #         ax2.barh(y_axis, x_axis, height=0.2)
    #     fig_name = f'poll_results_{poll.admin_key[:8]}.png'
    #     path = os.path.join(current_app.root_path, 'static/imgs/', fig_name)
    #     plt.savefig(path)
    # return fig_name


