import pyglet
import argparse
import urllib.request
import time
import getopt, sys
from PIL import Image
from io import BytesIO

class LocImage(object):
    # {location: [url, width, height]}  
    location = {}
    location["lavaredo"] = ['https://tl.scenaridigitali.com/trecime/images/image.jpg', 1920, 1080]
    location["pordoi"] = ['https://panodata.panomax.com/cams/1343/canazei_skiarea_belvedere.jpg', 1920, 1080]
    location["cinquetorri"] = ['https://s.skylinewebcams.com/webcam889.jpg', 289, 170]
    location["helbronner"]=["https://www.lovevda.it/Media/Cache/Webcam/big_courma2.jpg", 1280, 960]
    location["bianco_pano"]=["https://live-image.panomax.com/cams/1437/recent_reduced.jpg", 3445, 450]
    @classmethod
    def set_name(cls,name):
        cls.name = name
        return cls.name

    @classmethod
    def set_scale(cls,scale):
        cls.scale = scale
        return cls.scale
    
    @classmethod
    def get_url(cls):
        return cls.location[cls.name][0]
    
    @classmethod
    def get_width(cls):
        return cls.location[cls.name][1]

    @classmethod
    def get_height(cls):  
        return cls.location[cls.name][2]
    
    @classmethod 
    def get_scale(cls):
        return cls.scale
    
    @classmethod 
    def get_name(cls):
        return cls.name
    
    def __init__(self):
        super().__init__()
        
def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("-a" , "--list", help = "list all the available locations", action = "store_true")
    parser.add_argument("-l", "--location", help = "specify the location of the webcam", default = "lavaredo")
    parser.add_argument("-s", "--scale", type=float, help = "specify the scale of the displayed camera image", default = 1)
    
    args = parser.parse_args()

    if args.list:
        print("Available locations:")
        for key in LocImage.location.keys():
            print("\t" + key)
        exit(0)
        
    try:
        LocImage.location[args.location]
    except KeyError:
        print("Specified location is not avaiable\n")
        exit(0)
    
    

    if (args.scale < 0) or (args.scale > 5): 
        # max value 5 is just good sense. Correct max value should be driven by image and display resoliution 
        print("Invalid scale\n")
        exit(0)    
    
    LocImage.set_name(args.location)
    LocImage.set_scale(args.scale)
    
    # prepare the window for drawing
    window = pyglet.window.Window(fullscreen=False, width=LocImage.get_width()*LocImage.get_scale(), height=LocImage.get_height()*LocImage.get_scale())
    window.set_caption("Bonatti App " + "[" + LocImage.get_name() + "]")
    
    # == Stuff to render in the window
    @window.event
    def on_draw():
        img = get_raw_image(LocImage.get_url())     # pass the URL
        window.clear()
        image = pyglet.image.load('noname.raw', file=img)
        sprite = pyglet.sprite.Sprite(image) 
        sprite.scale = LocImage.get_scale()
        sprite.draw()
    
    @window.event
    def on_close():
        print("I'm closing now")
    
    @window.event
    def update(dt):
        window.dispatch_event('on_draw')
        print ("image updated")

    pyglet.clock.schedule_interval(update,60)   # refresh rate 60 sec
    pyglet.app.run()
    
def get_raw_image (url):
    # get data from URL
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_response = urllib.request.urlopen(req)
    img_data = web_response.read()
    img = (BytesIO(img_data))
    return img
        
if __name__ == "__main__":
    main(sys.argv)
    
