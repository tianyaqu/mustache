import tornado.web
import tornado.websocket
from PIL import Image
import StringIO
import numpy
import json
from solver import Solver

class Detector(tornado.websocket.WebSocketHandler):
      def __init__(self, *args, **kwargs):
            self.solver = Solver()
            super(Detector, self).__init__(*args, **kwargs)
        
      def open(self):
            print 'new connection'

      def on_message(self, message):
            image = Image.open(StringIO.StringIO(message))
            cv_image = numpy.array(image)
            if(cv_image.shape):
                self.process(cv_image)

      def on_close(self):
            print 'connection closed'

      def process(self, cv_image):
            loc = self.solver.solve(cv_image)
            print loc
            if (loc):
              result = json.dumps(loc)
            else:
              result = json.dumps((-1,-1,-1,-1))
            self.write_message(result)
