from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from novel_database import Novel, Base, Book, User
from flask import session as login_session
import random
import string
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Novels item-catalog"
engine = create_engine(
    'sqlite:///bookdata.db',
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    novel = session.query(Novel).all()
    book = session.query(Book).all()
    return render_template('login.html', STATE=state,
                           novel=novel, book=book)


# If user already logged
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                 json.dumps(
                                            'Current user already connected'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<center><h2><font color="green">Welcome '
    output += login_session['username']
    output += '!</font></h2></center>'
    output += '<center><img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; -webkit-border-radius: 200px;" '
    output += ' " style = "height: 200px;border-radius: 200px;" '
    output += ' " style = "-moz-border-radius: 200px;"></center>" '
    flash("you are now logged in as %s" % login_session['username'])
    print("Done")
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user_id


# Getting information of user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Getting user email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# To read novel JSON data on web browser
@app.route('/novel/JSON')
def novelJSON():
    novel = session.query(Novel).all()
    return jsonify(novel=[c.serialize for c in novel])


# To read novel wise of book JSON
@app.route('/novel/<int:novel_id>/main/<int:book_id>/JSON')
def novelListJSON(novel_id, book_id):
    book_list = session.query(Book).filter_by(id=book_id).one()
    return jsonify(Book_List=book_list.serialize)


# To read books JSON
@app.route('/novel/<int:book_id>/main/JSON')
def bookListJSON(book_id):
    novel = session.query(Novel).filter_by(id=book_id).one()
    book = session.query(Book).filter_by(book_id=novel.id).all()
    return jsonify(BookList=[i.serialize for i in book])


# This is home page of entire project
@app.route('/novel/')
def showNovel():
    novel = session.query(Novel).all()
    return render_template('novel.html', novel=novel)


# Create new novel
@app.route('/novel/new/', methods=['GET', 'POST'])
def newNovel():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newNovel = Novel(name=request.form['name'],
                         user_id=login_session['user_id'])
        session.add(newNovel)
        session.commit()
        return redirect(url_for('showNovel'))
    else:
        return render_template('newNovel.html')


# To edit existing novel name
@app.route('/novel/<int:novel_id>/edit/', methods=['GET', 'POST'])
def editNovel(novel_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedNovel = session.query(Novel).filter_by(id=novel_id).one()
    creater_id = getUserInfo(editedNovel.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this novel"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showNovel'))
    if request.method == 'POST':
        if request.form['name']:
            editedNovel.name = request.form['name']
            flash("Novel Successfully Edited %s" % (editedNovel.name))
            return redirect(url_for('showNovel'))
    else:
        return render_template('editNovel.html', novel=editedNovel)


# To delete existing novel
@app.route('/novel/<int:novel_id>/delete/', methods=['GET', 'POST'])
def deleteNovel(novel_id):
    if 'username' not in login_session:
        return redirect('/login')
    novelToDelete = session.query(Novel).filter_by(id=novel_id).one()
    creater_id = getUserInfo(novelToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot delete this novel"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showNovel'))
    if request.method == 'POST':
        session.delete(novelToDelete)
        flash("Successfully Deleted %s" % (novelToDelete.name))
        session.commit()
        return redirect(url_for('showNovel', novel_id=novel_id))
    else:
        return render_template('deleteNovel.html', novel=novelToDelete)


# It displays total book list of popular novels
@app.route('/novel/<int:novel_id>/book/')
def showBook(novel_id):
    novel = session.query(Novel).filter_by(id=novel_id).one()
    book = session.query(Book).filter_by(book_id=novel_id).all()
    return render_template('main.html', novel=novel, book=book)


# Create new novel
@app.route('/novel/<int:book_id>/new/', methods=['GET', 'POST'])
def newBookList(book_id):
    if 'username' not in login_session:
        return redirect('login')
    novel = session.query(Novel).filter_by(id=book_id).one()
    creater_id = getUserInfo(novel.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot add this book"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showNovel', novel_id=book_id))
    if request.method == 'POST':
        newList = Book(
            book_name=request.form['book_name'],
            author=request.form['author'],
            no_of_pages=request.form['no_of_pages'],
            genre=request.form['genre'],
            book_id=book_id,
            user_id=login_session['user_id']
            )
        session.add(newList)
        session.commit()
        flash("New Book List %s is created" % (newList))
        return redirect(url_for('showBook', novel_id=book_id))
    else:
        return render_template('newBookList.html', book_id=book_id)


# Editing particular novel book
@app.route('/novel/<int:novel_id>/<int:b_id>/edit/', methods=['GET', 'POST'])
def editBookList(novel_id, b_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedList = session.query(Book).filter_by(id=b_id).one()
    novel = session.query(Novel).filter_by(id=novel_id).one()
    creater_id = getUserInfo(editedList.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this novel"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showBook', novel_id=novel_id))
    if request.method == 'POST':
        editedList.book_name = request.form['book_name']
        editedList.author = request.form['author']
        editedList.no_of_pages = request.form['no_of_pages']
        editedList.genre = request.form['genre']
        session.add(editedList)
        session.commit()
        flash("Novel List has been edited!!")
        return redirect(url_for('showBook', novel_id=novel_id))

    else:
        return render_template('editBookList.html',
                               novel=novel, book=editedList)


# Deleting particular novel of book
@app.route('/novel/<int:book_id>/<int:list_id>/delete/',
           methods=['GET', 'POST'])
def deleteBookList(book_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    novel = session.query(Novel).filter_by(id=book_id).one()
    listToDelete = session.query(Book).filter_by(id=list_id).one()
    creater_id = getUserInfo(listToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this novel"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showBook', novel_id=book_id))
    if request.method == 'POST':
        session.delete(listToDelete)
        session.commit()
        flash("Novel list has been Deleted!!!")
        return redirect(url_for('showBook', novel_id=book_id))
    else:
        return render_template('deleteBookList.html', lists=listToDelete)


# Logout from application
@app.route('/disconnect')
def logout():
    access_token = login_session['access_token']
    print("In gdisconnect access_token is %s", access_token)
    print("User name is:")
    print(login_session['username'])

    if access_token is None:
        print("Access Token is None")
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(uri=url, method='POST', body=None,
                       headers={'Content-Type':
                                'application/x-www-form-urlencoded'})[0]
    print(result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out")
        return redirect(url_for('showBook'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
