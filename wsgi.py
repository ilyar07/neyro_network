from flaskapp import app
from waitress import serve

if __name__ == '__main__':
    print('WSGI running...')
    serve(app, host='localhost', port=80, threads=6)