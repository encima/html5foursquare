from app import app, db, models
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

print('---------SETUPCOMPLETE------')
print(app.config['ENV'])
if(app.config['ENV'].upper() == 'PRODUCTION'):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
elif(app.config['ENV'].upper() == 'DEVELOPMENT'):
    app.run(debug=True)
