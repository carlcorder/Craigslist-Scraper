from craigslist import CraigslistForSale
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

import props

geolocator = Nominatim()
orig_coord = (0, 0)

# initializing the originating location
def init_orig():
    orig_loc = geolocator.geocode(props.ORIG_LOC)
    global orig_coord
    orig_coord = (orig_loc.latitude, orig_loc.longitude)

# calculates the distance in miles between two locations
def get_distance(orig_coord, dest):
    dest_loc = geolocator.geocode(dest)
    dest_coord = (dest_loc.latitude, dest_loc.longitude)
    return round(vincenty(orig_coord, dest_coord).miles, 1)

# display formatted results
def display_results(result):
    dest = result['where'] + ", " + props.ORIG_STATE
    print result['name'] + " " + result['price'] + " " + result['where']
    print "distance: " + str(get_distance(orig_coord, dest)) + " miles\n"

init_orig()
cl_fs = CraigslistForSale(site=props.CRAIG_SITE, category=props.CRAIG_CATEGORY,
                          filters={'max_price': props.CRAIG_PRICE, 'has_image': props.CRAIG_IMAGE})

for result in cl_fs.get_results(sort_by=props.CRAIG_SORTBY):
    if props.CRAIG_SITE in result['url']:
        display_results(result)