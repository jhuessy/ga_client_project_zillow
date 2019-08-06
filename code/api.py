#HEAVILY INDEBTED TO https://towardsdatascience.com/deploying-a-keras-deep-learning-model-as-a-web-application-in-p-fc0f2354a7ff
# FOR CODE INSPIRATION
#IMPORTS
from flask import Flask, request, render_template
from test import *
from buildings import *
from rform import *
from flask import jsonify
from jinja2 import Template
import os
from zipreport import *
#SET UP APP AND ADD SECRET KEY/CACHING PARAMETERS
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# HOME PAGE ROUTE
@app.route("/zip/", methods=['GET', 'POST'])
def home():
    # CREATE FORM FROM FORM CLASS IN RFORM SCRIPT
    form = ReusableForm()
    # IF FORM VALIDATES WHEN SUBMITTED
    if form.validate_on_submit():
        # GET ZIPCODE FROM FORM
        zipcode = request.form['zipcode']
        # GET REPORT ELEMENTS FROM ZIPREPORT SCRIPT
        input,script,div=get_report(zipcode=zipcode)
        # RENDER REPORT TEMPLATE WITH ELEMENTS FROM SCRIPT
        return render_template('report.html',
                               input=input,script=script,div=div)
    # IF FORM FAILS TO VALIDATE
    elif form.validate()==False:
        #CURRENTLY NOT WRITING ANYTHING TO LOG
        print("")
    # RENDER HOME PAGE FROM TEMPLATE AND FORM OBJECT
    return render_template('index.html', form=form)

# API ROUTES - DEPRECATED IN FINAL VERSION
#ADDRESSES
@app.route('/api/addresses/', methods=['GET'])
def addresses():
    #READ IN REQUEST ARGUMENTS
    reqargs = request.args.to_dict()
    #PULL ZIPCODE AND STATE FROM REQUEST ARGUMENTS
    zipcode = reqargs['zipcode']
    state = reqargs['state']
    # GET ADDRESSES FROM ADDRESS SCRIPT
    results = get_address(zipcode,state)
    # RETURN AS JSON
    return jsonify(results)
@app.route('/api/buildings/',methods=['GET'])
# BUILDINGS
def buildings():
    #READ IN REQUEST ARGUMENTS
   reqargs = request.args.to_dict()
   #PULL ZIPCODE FROM REQUEST ARGUMENTS
  zipcode = reqargs['zipcode']
  # GET BUILDINGS TOTAL FROM BUILDINGS SCRIPT
   results = get_buildings(zipcode)
     # RETURN AS JSON
  return jsonify(results)

#RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

#INSPIRED BY https://stackoverflow.com/questions/45583828/python-flask-not-updating-images
# FORCES BROWSERS TO REFRESH STATIC IMAGES
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
