
from handlers_api import handlers
import tornado.log
import tornado.httpserver
import tornado.ioloop
import tornado.web

def main():
    settings = {
        'debug':True,
        'compress_response':True
    }


    app = tornado.web.Application(handlers, **settings)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888, '127.0.0.1')
    tornado.log.enable_pretty_logging()

    app.dbm = None



    try:
        server.start()
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    main()
