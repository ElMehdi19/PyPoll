from flask import Blueprint, make_response, request, url_for, flash
from flask_restful import Api, Resource, reqparse
from FlaskApp import db
from FlaskApp.dbModels import Poll
from datetime import datetime

apis = Blueprint('apis', __name__)
api = Api(apis)

class PollAPI(Resource): # http://127.0.0.1:5000/api/1.0/poll/{id}?token=

    # THIS RESOURCE IS RESPONSIBLE OF EVERYTHING RELATED TO DATA OF A SINGLE POLL
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('options', type=list, location='json')
        self.reqparse.add_argument('start_date', type=str, location='json')
        self.reqparse.add_argument('end_date', type=str, location='json')
        self.reqparse.add_argument('guestsAllowed', type=bool, location='json')
    def get(self, id):
        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'Not found'}, 404)
        req_args = request.args
        admin_key = req_args.get('token')
        if poll.admin_key != Poll.check_token(admin_key):
            return make_response({'status':'error', 'message':'Unauthorized'}, 403)

        # TURNING THE POLL INSTANCE INTO A DICT AND REMOVING UNNESSECARY INFORMATION (eg. admink_key)
        
        poll_data = poll.__dict__
        unwanted = ['admin_key', '_sa_instance_state']
        for key in unwanted:
            del poll_data[key]
        settings = ['isLive', 'isCompleted', 'guestsAllowed']
        poll_settings = {}
        for key in settings:
            poll_settings[key] = poll_data[key]
            del poll_data[key]
        poll_data['settings'] = poll_settings
        poll_data['options'] = list(poll_data['options'].keys())
        poll_data['ballot'] = url_for('poll.pollView', id=id, _external=True)
        poll_data['formated_dates'] = {
            'starts' : poll.start_date.strftime('%m/%d/%y %H:%M'),
            'ends' : poll.end_date.strftime('%m/%d/%y %H:%M')
        }
        return make_response({'status':'success', 'poll': poll_data}, 200)
    def post(self, id):

        # THIS METHOD IS FOR GIVING THE ADMIN ACCESS TO THE POLL DASHBOARD TO MANAGE IT
        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'not found'}, 404)
        args = self.reqparse.parse_args()
        token = args['token']
        if poll.admin_key != token:
            return make_response({'status':'error', 'message':'Invalid Key'}, 403)
        response = make_response({'status':'success'}, 200)
        admin_cookie = poll.get_token('admin')
        response.set_cookie('authenticated', admin_cookie)
        return response
    def put(self, id):

        # THIS METHOD IS RESPONSIBLE OF UPDATING THE POLL INFORMATION
        # ACCESSIBLE ONLY IF THE POLL IS NOT LIVE YET

        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'not found'}, 404)
        args = self.reqparse.parse_args()
        token = args['token']
        if Poll.check_token(token) != poll.admin_key:
            return make_response({'status':'error', 'message':'Unauthorized key'}, 403)
        del args['token']

        # CHECKING IF THE POLL IS LIVE 
        if poll.isLive:
            return make_response({'status':'error', 'message':'Poll is already live.'}, 403)
        params = ['title','options','start_date','end_date','guestsAllowed']

        # CHECKING IF ALL THE FIELDS HAVE VALUES
        if not all([param in args.keys() for param in params]):
            return make_response({'status':'error', 'message':'fields missing'}, 400)
        
        # CHECKING IF THERE ARE AT LEAST 2 OPTIONS
        if len(args['options']) < 2:
            return make_response({'status':'error', 'message':'add more options'}, 400)
        
        # CHECKING IF THE SPECIFIED DATE FORMAT IS ELIGIBLE AND NOT PAST DUE
        try:
            if any([datetime.utcnow() >= datetime.strptime(args[date], '%m/%d/%y %H:%M') for date in params[2:4]]):
                raise Exception
        except ValueError:
            return make_response({'status':'date_error', 'message':'Invalid date format.'}, 400)
        except Exception:
            return make_response({'status':'date_error', 'message':'Date is past due.', 'current_date':datetime.utcnow()}, 400)
        
        # CHECKING IF ANY FIELD IS EMPTY AND RETURNING AN ERROR IF SO

        poll_obj = poll.__dict__
        empty_fields = []
        for key, val in args.items():
            if poll_obj[key] != val: # CHECKS IF THE NEW VALUE IS ALREADY IN DATABASE TO AVOID UNNECESSARY UPDATES
                if not val:
                    empty_fields.append(key)
                    break
                if key in params[2:4]: # CHECKS IF THE VALUE IS A DATE
                    val = datetime.strptime(val, '%m/%d/%y %H:%M')
                setattr(poll, key, val if key != 'options' else { option:0 for option in val } )
        if empty_fields:
            return make_response({'status':'fields_error', 'fields':empty_fields, 'message':'fields missing'}, 400)
        
        # ANYTHING PAST THIS LINE IS A SUCCESS RESPONSE
        
        db.session.commit()
        flash('Poll Updated', 'success')
        return make_response({'status':'success', 'message':'poll updated.'}, 200)
        

class VoteAPI(Resource): # http://127.0.0.1:5000/api/1.0/vote/2?token=89ea31466a18119b

    # THIS RESOURCE IS RESPONSIBLE OF ANYTHING THAT HAS TO DO WITH THE VOTING OPERATION
    # GETTING POLL OPTIONS AND SUBMITING VOTES

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('vote', type=str, location='json')
    def get(self, id):
        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'not found'}, 404)
        # args = self.reqparse.parse_args()
        args = request.args

        # CHECKING IF GUESTS ARE ALLOWED 
        if not poll.guestsAllowed:
            # CHECKING IF THE PROVIDED KEY MATCHES THE POLL PUBLIC KEY AND GRANTING ACCESS TO VOTING AREA IF SO.
            if poll.public_key != args['token']:
                return make_response({'status':'error', 'message':'Invalid key'}, 403)
        response = { 'poll_title': poll.title, 'poll_options': list(poll.options.keys()) }
        return make_response({'status':'success', 'poll': response}, 200)

    def put(self, id):
        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'not found'}, 404)
        args = self.reqparse.parse_args()

        # CHECKING IF THE POLL IS LIVE
        if not poll.isLive:
            return make_response({'status':'error', 'message':'poll is not live yet'}, 403)
        
        # CHECKING IF GUESTS ARE ALLOWED IN THIS POLL
        if not poll.guestsAllowed:
            # CHECKING IF THE PROVIDED KEY MATCHES THE POLL PUBLIC KEY AND GRANTING ACCESS TO VOTING AREA IF SO.
            if poll.public_key != args['token']:
                return make_response({'status':'error', 'message':'Invalid key'}, 403)
        
        # CHECKING IF THIS POLL IS NOT YET DONE AND RETURNING A 403 RESPONSE IF NOT
        if poll.isCompleted:
            return make_response({'status':'error', 'message':'voting completed'}, 403)
        
        # CHECKING IF THE USER HAS SUBMITTED AN OPTION
        try:
            if any(['vote' not in args.keys(), not args['vote']]):
                return make_response({'status':'error', 'message':'no option was selected'}, 400)
        except Exception:
            pass

        # CHECKING IF THE SUBMITTED OPTION IS ELIGIBLE
        if args['vote'] not in poll.options.keys():
            return make_response({'status':'error', 'message':'Invalid option'}, 400)
        
        # ALTERING THE OPTIONS COLUMN IN THE SPECIFIED POLL AND SUCCESS RESPONSE
        poll.votes += 1
        options = dict(poll.options)
        options[args['vote']] += 1
        poll.options = options
        db.session.commit()
        return make_response({'status':'success', 'end_date':poll.end_date}, 201)


class VoteResultsAPI(Resource): # http://127.0.0.1:5000/api/1.0/results/{id}
    
    # THIS RESOURCE IS RESPONSIBLE OF THE FINAL RESULTS 

    def get(self, id):
        poll = Poll.query.get(id)
        if not poll:
            return make_response({'status':'error', 'message':'not found'}, 404)

        # CHECKING IF THE POLL IS STILL LIVE AND RETURNING 403 RESPONSE IF SO
        if poll.isLive or not poll.isCompleted:
            return make_response({'status':'error', 'message':'can not fetch the results now, try later.'}, 403)
        
        # FETCHING THE RESULTS FROM THE DATABASE
        options = poll.options

        # SORTING THE RESULTS FROM GREATER TO LOWER TO PLOT THEM IN THE CLIENTSIDE USING CHARTJS

        results = { key:options[key]  for key in sorted(options, key=options.get)}
        total = VoteResultsAPI.format_votes(poll.votes)
        csv = poll.csv_results
        return make_response({'status':'success', 'title':poll.title, 'results':results, 'total':total, 'csv':csv}, 200)
    
    @staticmethod
    def format_votes(number):

        # THIS STATIC METHOD WILL MAKE THE TOTAL NUMBER OF VOTES LOOK MORE READABLE, (i.e: 100000 => 100,000)
        to_str = str(number)
        result = []
        while to_str:
            result.append(to_str[:3])
            to_str = to_str[3:]
        result = [f'{num}_' for num in result]
        result = int(''.join(result).strip('_'))
        return f'{result:,}'
    
api.add_resource(PollAPI, '/api/1.0/poll/<int:id>', endpoint='poll')
api.add_resource(VoteAPI, '/api/1.0/vote/<int:id>', endpoint='vote')
api.add_resource(VoteResultsAPI, '/api/1.0/results/<int:id>', endpoint='results')
