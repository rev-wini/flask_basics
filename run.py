from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


# app.config is a general purpose python dictionary to define environment variables for database and project
# secret_key is used by flask to secure data inside the user sessions, forms, cookies etc
app.config.update(
                    SECRET_KEY='mysecretkey',
                    SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost:5433/catalog_db',
                    SQLALCHEMY_TRACK_MODIFICATIONS=False
                    )

db = SQLAlchemy(app)


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Name is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True) # path to the image
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, format, image, num_pages, pub_id):
        # do not include pub_date because pub_date will be populated automatically as we set default value for pub_date above
        # not include book id - in SQLAlchemy, unless we specify otherwise the value for primary keys are populated automatically
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


# flask allows us to define more than one route per function
@app.route('/index')
@app.route('/')
def hello_flask():
    return "hello flask"


# with query string
# in browser, will need to type: /new/?greeting=hola
@app.route('/new/') # note the '/' at the end
def query_strings(greeting='hey'): # add default value here
    query_val = request.args.get('greeting', greeting)  # need to put the default here too
    return '<h1> the greeting is : {} </h1>'.format(query_val)


# remove query string
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='mina'):
    return '<h1> hello there ! {} </h1>'.format(name)


# strings
@app.route('/text/<string:name>')
def working_with_string(name):
    return '<h1>Here is a string ' + name + '</h1>'


# numbers - required entry in the browser to be integer, if entered string, will get error
# only integers are allowed
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1>Here is a number ' + str(num) + '</h1>'


# numbers
@app.route('/number/<string:num>')
def working_with_number(num):
    return '<h1>Here is a number ' + num + '</h1>'


@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    # return '<h1>Here is a number ' + str(num1 + num2) + '</h1>'
    return '<h1>Here is the sum {}'.format(num1+num2) + '</h1>'


# ensure entries are float
@app.route('/add/<float:num1>/<float:num2>')
def product_floats(num1, num2):
    # return '<h1>Here is a number ' + str(num1 + num2) + '</h1>'
    return '<h1>Here is the product {}'.format(num1*num2) + '</h1>'


# using templates
# flask will look for html in the "templates" folder automatically
@app.route('/temp')
def using_templates():
    return render_template('hello.html', name="Minia", age=35)


# Jinja templates - list
@app.route('/watch')
def top_movies():
    movie_list = ['abc', 'dcf', 'ere', 'ageeae', 'egagaered']
    return render_template('movies.html', movies=movie_list, name='Harry')


# Jinja templates - dict
@app.route('/tables')
def movies_plus():
    movie_dict = {'abc': 2.04, 'dcf': 3.4, 'ere': 8.3, 'bcd': 4.5, 'ega': 5.3}
    return render_template('table_data.html', movies=movie_dict, name='Sally')


# filters
@app.route('/filters')
def filter_data():
    movie_dict = {'abc': 2.04, 'dcf': 3.4, 'ere': 8.3, 'bcd': 4.5, 'ega': 5.3}
    return render_template('filter_data.html', movies=movie_dict, name=None, film='christmas carol')


# macros
@app.route('/macros')
def jinja_macros():
    movie_dict = {'abc': 2.04, 'dcf': 3.4, 'ere': 8.3, 'bcd': 4.5, 'ega': 5.3}
    return render_template('using_macros.html', movies=movie_dict)


if __name__ == "__main__":
    db.create_all() # only if table not exist yet, skipped if already exist
    app.run(debug=True)