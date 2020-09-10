import logging
logging.basicConfig(filename='log.txt', filemode='w')
from flask import Flask, request
# import pandas as  pd
import app_functions
import utils
from fb import db as dbreference

#### Setting up
# df = pd.read_csv('data.csv')
qt = utils.make_danger_quad_tree(dbreference.child('crime').get())
sos_qt = utils.make_sos_quad_tree(dbreference.child('sos_location').get())
# sos_qt = #make another quad tree


#### API functions below

app = Flask('InsertACoolNameHere')

@app.route('/nearby')
def nearby():
    args = request.args
    lat = float(args['lat'])
    long = float(args['long'])

    list_of_dangerous = app_functions.get_nearby(qt, lat, long)
    app.logger.info(list_of_dangerous)

    data = {
        'data':[]
        }
    for coods in list_of_dangerous:
        data['data'].append(
                {
                    'x':coods['latitude'],
                    'y':coods['longitude'],
                    'description':coods['crime'],
                    'precautions':coods['precautions']
                }
            )
    return data

@app.route('/routes')
def enroute_unsafe():
    args = request.args
    lat1 = float(args['lat1'])
    long1 = float(args['long1'])
    lat2 = float(args['lat2'])
    long2 = float(args['long2'])

    list_of_dangerous = app_functions.enroute(qt, lat1, long1, lat2, long2)
    app.logger.info(list_of_dangerous)

    data = {
        'data':[]
        }
    for coods in list_of_dangerous:
        data['data'].append(
                {
                    'x':coods['latitude'],
                    'y':coods['longitude'],
                    'description':coods['crime'],
                    'precautions':coods['precautions']
                }
            )    
    return data

@app.route('/crime')
def crime_mark():
    args = request.args
    lat = float(args['lat'])
    long = float(args['long'])
    crime = args['crime']

    app_functions.mark_crime(qt, lat, long, crime)

    return {'success':True}

@app.route('/sos')
def send_sos():
    args = request.args
    lat = float(args['lat'])
    long = float(args['long'])
    print(lat, long)
    try:
        phone = args['phone']
    except Exception as e:
        phone = '8350925585'

    result = app_functions.send_sos(sos_qt, lat, long, phone)
    return {'success':True, 'nearby':result}

@app.route('/register')
def register_sos_place():
    args = request.args
    lat = float(args['lat'])
    long = float(args['long'])
    email = args['email']

    app_functions.create_sos_location(sos_qt, lat, long, email)
    return {'success':True}

@app.route('/show_qt')
def show_qt():
    # print(qt)
    return str(qt.show())

@app.route('/show_sos_qt')
def show_sos_qt():
    # print(qt)
    return str(sos_qt.show())


@app.route('/')
def home():
    msg = 'Team InsertACoolNameHere'
    return msg


if __name__=='__main__':
    app.run('0.0.0.0', port=1234, debug=True)
