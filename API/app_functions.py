import quad, utils
from fb import db as dbreference
import time

query_range = 0.07207 / 4
# query_range = 6


def get_nearby(qt, lat, long):
    '''
    Get the unsafe areas near a location
    '''
    cell = quad.cell(abs(lat), abs(long), query_range, query_range)
    results = qt.query(cell)
    return [result.to_dict() for result in results]


def enroute(qt,lat1, long1, lat2, long2):
    '''
    Get the unsafe areas between two points on the map
    '''
    # distance = utils.distance(lat1, long1, lat2, long2)
    # print(distance)
    cell = quad.cell(abs(lat1), abs(long1), abs(lat2-lat1), abs(long2-long1))
    print(cell)
    results = qt.query(cell)
    print(len(results))
    return [result.to_dict() for result in results]

def mark_crime(qt, lat, long, crime):
    '''
    Add a crime to database and quad tree
    '''
    utils.insert_to_qt(qt, lat, long, crime)

    dbreference.child('crime').push(
        {'crime':crime,'latitude':lat, 'longitude':long}
        )

    # with open('data.csv', 'a+') as file:
    #     with csv.writer(file) as csvwriter:
    #         csvwriter.write_row((lat, long, crime,))

def send_sos(sos_qt, lat, long, phone):
    '''
    Send SOS to nearby police stations and hospitals
    '''
    cell = quad.cell(abs(lat), abs(long), query_range, query_range)
    results = sos_qt.query(cell)
    # print(len(results))
    tries=0
    qr = query_range*2
    while len(results)<0 or tries<5:
        # double the radius of searching for police and 
        # hospitals if there are no results get_nearby
        # until you find some or 5 retries
        cell = quad.cell(abs(lat), abs(long), qr, qr)
        results = sos_qt.query(cell)
        tries+=1
        qr*=2
    print(len(results))
    details = [result.email for result in results]
    mark_sos(details, lat, long, phone)
    return details

def mark_sos(locations, lat, long, phone):
    for location in locations:
        location = location.replace('@','%').replace('.','%')

        time_ref = int(time.time())

        phone = phone.lstrip('+91')
        bloodgroup = dbreference.child('user').child(phone).child('bloodgroup').get().val()

        dbreference.child('sos_location').child(location).child('sos').child(str(time_ref)).set({'lat':lat, 'long':long, 'timestamp':time_ref, 'phone':phone, 'bloodgroup':bloodgroup})

def create_sos_location(sos_qt, lat, long, email):
    '''
    Register a new hospital or police station
    '''
    utils.insert_to_sos_qt(sos_qt, lat, long, email)        