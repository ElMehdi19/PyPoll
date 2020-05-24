from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from datetime import datetime

class newPollForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()],
                            render_kw={'placeholder':'Email Address'})
    title = TextAreaField('Question?', validators=[DataRequired(), Length(min=3)],
                            render_kw={'placeholder':'What\'s the best TV Show ever?'})
    option1 = StringField('', validators=[DataRequired()],
                            render_kw={'placeholder':'Game Of Thrones'})
    option2 = StringField('', validators=[DataRequired()],
                            render_kw={'placeholder':'Mr. Robot'})
    start_date  = StringField('Starting date (blank to start immidiately)',
                            render_kw={'placeholder':'mm/dd/yy hh:mm', 
                                        'title':datetime.utcnow().strftime('%m/%d/%y %H:%M')})
    end_date    = StringField('Ending date', validators=[DataRequired()],
                            render_kw={'placeholder':'mm/dd/yy hh:mm'})
    guests  = BooleanField('Allow guests')
    submit  = SubmitField('Create Poll')
    
    def validate_start_date(self, start_date):
        if start_date.data:
            try:
                date = datetime.strptime(start_date.data, '%m/%d/%y %H:%M')
                if datetime.now() > date:
                    raise Exception
            except ValueError:
                raise ValidationError('This date doesn\'t match the specified format.')
            except Exception:
                raise ValidationError('This date is past due.')
        
    
    def validate_end_date(self, end_date):
        try:
            date = datetime.strptime(end_date.data, '%m/%d/%y %H:%M')
            if datetime.now() > date:
                raise Exception
        except ValueError:
            raise ValidationError('This date doesn\'t match the specified format.')
        except Exception:
            raise ValidationError('This date is past due.')

