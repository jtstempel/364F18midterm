###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
import requests
import pprint
import json
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy

## App setup code
app = Flask(__name__)
app.debug = True

## All app.config values

app.config['SECRET_KEY'] = 'si364hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://josephtstempel@localhost/jstempelMidterm'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################


consumer_key = "YQj6yyIQh9uN2QAnkmGM49NVXcpWxeBD"
consumer_secret = "ERAyoAfAMHG2Y0CR"


##################
##### MODELS #####
##################

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    genre = db.Column(db.String)
    venue_id = db.Column(db.String, db.ForeignKey('venues.id'))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Venue(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    postal_code = db.Column(db.String)

    def __repr__(self):
        return '{} | ID: {}'.format(self.name, self.id)


###################
###### FORMS ######
###################


class CityForm(FlaskForm):
    name_city = StringField('Please enter the name of a city: ', validators = [Required()])
    submit = SubmitField('Submit')

class KeywordForm(FlaskForm):
    keyword_search = StringField('Please enter a keyword (no special characters): ', validators = [Required()])
    submit = SubmitField('Submit')

    def validate_keyword_search(self, field):
        special_characters = ['@','#','%','*','?','/']
        for letter in special_characters:
            if letter in self.keyword_search.data:
                raise ValidationError('Your keyword was invalid because it contained a special character')
            

#######################
###### VIEW FXNS ######
#######################


@app.route('/city_entry')
def city_entry():
    my_form = CityForm()
    return render_template('city_entry.html', form = my_form)

@app.route('/city_result', methods = ['GET', 'POST'])
def city_result():
    form = CityForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name_city = form.name_city.data
        base_url = "https://app.ticketmaster.com/discovery/v2/events.json?"
        my_params = {}
        my_params['city'] = name_city
        my_params['apikey'] = consumer_key
        my_params['size'] = 10
        response = requests.get(base_url, params = my_params)
        object_json = json.loads(response.text)
        list_results = []
        if '_embedded' not in object_json:
            return render_template('event_data.html', list_results = list_results, name_city = name_city)
        json_response = object_json['_embedded']['events']
        
        
        for each_event in json_response:
            
            if Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first():
                venue = Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first()
                
                if Event.query.filter_by(id = each_event['id']).first():
                    event = Event.query.filter_by(id = each_event['id']).first()
                else:
                    event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                    db.session.add(event)
                    db.session.commit()

            else:
                venue = Venue(id = each_event['_embedded']['venues'][0]['id'], name = each_event['_embedded']['venues'][0]['name'], url = each_event['_embedded']['venues'][0]['url'], postal_code = each_event['_embedded']['venues'][0]['postalCode'])
                db.session.add(venue)
                db.session.commit()

                event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                db.session.add(event)
                db.session.commit()
            list_results.append((event.name, event.url, event.genre, venue.name))

        return render_template('event_data.html', list_results = list_results, name_city = name_city)

    flash('All fields are required!')
    return redirect(url_for('city_entry'))




@app.route('/keyword_search', methods = ["GET"])
def keyword_search():
    keyword_form = KeywordForm(request.args)
    list_results = None
    if request.method == "GET" and keyword_form.validate():
        my_keyword = keyword_form.keyword_search.data
        base_url = "https://app.ticketmaster.com/discovery/v2/events.json?"
        my_params = {}
        my_params['keyword'] = my_keyword
        my_params['apikey'] = consumer_key
        my_params['size'] = 10
        response = requests.get(base_url, params = my_params)
        object_json = json.loads(response.text)
        if '_embedded' not in object_json:
            return render_template('keyword_entry.html', list_results = list_results, form = keyword_form)
        json_response = object_json['_embedded']['events']
        list_results = []
        
        for each_event in json_response:
            if Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first():
                venue = Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first()
                
                if Event.query.filter_by(id = each_event['id']).first():
                    event = Event.query.filter_by(id = each_event['id']).first()
                else:
                    event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                    db.session.add(event)
                    db.session.commit()

            else:
                venue = Venue(id = each_event['_embedded']['venues'][0]['id'], name = each_event['_embedded']['venues'][0]['name'], url = each_event['_embedded']['venues'][0]['url'], postal_code = each_event['_embedded']['venues'][0]['postalCode'])
                db.session.add(venue)
                db.session.commit()

                event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                db.session.add(event)
                db.session.commit()
            list_results.append((event.name, event.url, event.genre, venue.name))


    errors = [v for v in keyword_form.errors.values()]
    if len(errors) > 0:
        flash("There was an error in the form submission! - " + str(errors))


    return render_template('keyword_entry.html', list_results = list_results, form = keyword_form)

@app.route('/keyword_search/<keyword_entry>', methods = ['GET'])
def dynamic_url(keyword_entry):
    list_results = None
    if request.method == "GET":
        my_keyword = keyword_entry
        base_url = "https://app.ticketmaster.com/discovery/v2/events.json?"
        my_params = {}
        my_params['keyword'] = my_keyword
        my_params['apikey'] = consumer_key
        my_params['size'] = 10
        response = requests.get(base_url, params = my_params)
        object_json = json.loads(response.text)
        if '_embedded' not in object_json:
            return render_template('keyword_entry.html', list_results = list_results, form = None)
        json_response = object_json['_embedded']['events']
        list_results = []

        for each_event in json_response:
            if Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first():
                venue = Venue.query.filter_by(id = each_event['_embedded']['venues'][0]['id']).first()
                
                if Event.query.filter_by(id = each_event['id']).first():
                    event = Event.query.filter_by(id = each_event['id']).first()
                else:
                    event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                    db.session.add(event)
                    db.session.commit()

            else:
                venue = Venue(id = each_event['_embedded']['venues'][0]['id'], name = each_event['_embedded']['venues'][0]['name'], url = each_event['_embedded']['venues'][0]['url'], postal_code = each_event['_embedded']['venues'][0]['postalCode'])
                db.session.add(venue)
                db.session.commit()

                event = Event(id = each_event['id'], name = each_event['name'], url = each_event['url'], genre = each_event['classifications'][0]['genre']['name'], venue_id = venue.id)
                db.session.add(event)
                db.session.commit()
            list_results.append((event.name, event.url, event.genre, venue.name))
 
    return render_template('keyword_entry.html', list_results = list_results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


## Code to run the application...

if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
