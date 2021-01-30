import pyglet
import urllib.request
import time
import getopt, sys
from PIL import Image
from io import BytesIO

# BAD: use of a global variable
location_name = ""

# TODO: class for handling getter and setter on location 

def main(argv):
    location_name = argv[1]
    my_data = get_location_image_data(location_name)
    my_width = my_data[1]
    my_height = my_data[2]
    
    # prepare the window for drawing
    window = pyglet.window.Window(fullscreen=False, width=my_width, height=my_height)
    # == Stuff to render the image:
    @window.event
    def on_draw():
        my_data = get_location_image_data(location_name)    # still duplicate code to fix
        img = get_raw_image(my_data[0])
        window.clear()
        image = pyglet.image.load('noname.raw', file=img)
        sprite = pyglet.sprite.Sprite(image) 
        sprite.draw()
    
    @window.event
    def on_close():
        print("I'm closing now")
    
    @window.event
    def update(dt):
        window.dispatch_event('on_draw')
        print ("Updated Image")
    
    pyglet.clock.schedule_interval(update,60)
    pyglet.app.run()
    
# TODO: refactor with class for location data 

def get_location_image_data(name):
    # {location: [url, width, height]}
    # TODO: read location data from a config file 
    location = {}
    location["lavaredo"] = ['https://tl.scenaridigitali.com/trecime/images/image.jpg', 1920, 1080]
    location["pordoi"] = ['https://panodata.panomax.com/cams/1343/canazei_skiarea_belvedere.jpg', 1920, 1080]
    return location[name]

def get_raw_image (url):
    # get data from URL
    web_response = urllib.request.urlopen(url)
    img_data = web_response.read()
    img = (BytesIO(img_data))
    return img

def scale_image(img):
    # TODO:
    return
        
if __name__ == "__main__":
    main(sys.argv)
    
