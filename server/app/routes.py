from app import app

@app.route('/')
@app.route('/index')
def index():
    print('test')
    return 'test'
