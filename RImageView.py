import pyglet,urllib.request,time, getopt, sys
from PIL import Image
from io import BytesIO

location_name = ""

# TODO: class for handling getter and setter on location 

def main(argv):
    location_name = argv[1]
    my_data = get_location_data(location_name)
    my_width = my_data[1][0]
    my_height = my_data[1][1]
    
    window = pyglet.window.Window(fullscreen=False, width=my_width, height=my_height)
    # == Stuff to render the image:
    @window.event
    def on_draw():
        my_data = get_location_data(location_name)
        window.clear()
        img = my_data[0]
        image = pyglet.sprite.Sprite(pyglet.image.load('noname.png', file=img)) 
        image.draw()
    
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

def get_location_data(name):
    # {location: [url, width, height]}
    location = {}
    location["lavaredo"] = ['https://tl.scenaridigitali.com/trecime/images/image.jpg', 1920, 1080]
    location["pordoi"] = ['https://vcdn.bergfex.at/webcams/archive.new/downsized/2/10882/2021/01/29/10882_2021-01-29_0915_688d47e0ed941b8b.jpg', 1280, 960]
    
    # get data from URL
    web_response = urllib.request.urlopen(location[name][0])
    
    img_data = web_response.read()
    img = (BytesIO(img_data))
    res = [location[name][1], location[name][2]]
    return img, res

def load_remote_image():
    
    # TODO: add information about image resolution
    img_urls = []
    img_urls.append('https://tl.scenaridigitali.com/trecime/images/image.jpg')
    img_urls.append('https://vcdn.bergfex.at/webcams/archive.new/downsized/2/10882/2021/01/29/10882_2021-01-29_0915_688d47e0ed941b8b.jpg')
    
    web_response = urllib.request.urlopen(img_urls[1])
    img_data = web_response.read()
    img = (BytesIO(img_data))
    return img

if __name__ == "__main__":
    main(sys.argv)
    
