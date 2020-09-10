from math import cos, asin, sqrt
from fb import db as dbreference
import quad

# centre coods of India
centre_x, centre_y, half_w, half_h = 21.2106, 82.7948, 14.5, 14.6008
query_range = 0.07207 / 4

from quadtrees import Danger, SOS

crime_precautions_map = {
    }

def insert_to_qt(qt, lat, long, crime):
    location = Danger(lat, long, crime)
    # print('done')
    qt.insert(location)
    

def insert_to_sos_qt(qt, lat, long, email):
    location = SOS(lat, long, email)
    qt.insert(location)
    # dbreference.child('police').push(
    #     {'email':email,'latitude':lat, 'longitude':long}
    #     )

def series_to_qt(row):
    return Danger(row['latitude'], row['longitude'], row['crime'],
                  crime_precautions_map.get(row['crime'], '')
                  )

def fb_to_qt(row):
    # print('------')
    # print(row)
    return Danger(row['latitude'], row['longitude'], row['crime'],
                  crime_precautions_map.get(row['crime'], '')
                  )

def fb_to_sos_qt(row):
    return SOS(float(row['location']['latitude']), float(row['location']['longitude']), row['email']
                  )


def make_danger_quad_tree(fb):
    """
    df: Dataframe -> (Quad Tree)
    """
    complete_cell = quad.cell(centre_x, centre_y, half_w, half_h)
    # print(complete_cell)
    qt = quad.quad_tree(complete_cell)

    for item in fb.each():
        # print(item.val())
        if item.val()==None:
            continue
        rest = fb_to_qt(item.val())
        qt.insert(rest)
    # print(qt.show())
    return qt

def make_sos_quad_tree(fb):
    """
    df: Dataframe -> (Quad Tree)
    """
    complete_cell = quad.cell(centre_x, centre_y, half_w, half_h)
    # print(complete_cell)
    sos_qt = quad.quad_tree(complete_cell)
    # print('**************')

    for item in fb.each():
        # print(item.val())
        if item.val()==None:
            continue
        rest = fb_to_sos_qt(item.val())
        # print(rest)
        sos_qt.insert(rest)
    # print(sos_qt.show())
    return sos_qt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )
    dist = 12742 * asin(sqrt(a))

    return dist
