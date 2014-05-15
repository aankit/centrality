import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from centrality import Centrality
from tornado.options import define, options

define("port", default=5000,help="run on the given port", type=int)

tornado.options.parse_command_line()

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class CentralityHandler(tornado.web.RequestHandler):
	def get(self):
		response = self.get_argument("word")
		c = Centrality(response)
		for line in c.writePoem():
			print line
			self.write(line)

static_path = os.path.join(os.path.dirname(__file__), "static")
template_path = os.path.join(os.path.dirname(__file__), "templates")
application = tornado.web.Application(
	handlers=[(r"/", IndexHandler), (r"/poem", CentralityHandler)],
	static_path=static_path,
	template_path=template_path)

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(options.port)
tornado.ioloop.IOLoop.instance().start()