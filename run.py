from app import init_app
from db import

db.init_app(app)

#before the first request runs, it runs the below method
@app.before_first_request
def create_tables():
    #creates 'sqlite:///data.db'
    #only creates tables it sees (goes through imports)
    db.create_all()
