from flask import Flask, render_template, url_for, redirect, request, jsonify, flash, session
from data import queries, data_manager, auth
from flask_cors import CORS
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')
CORS(app)
app.secret_key = '0e7481098709f45cf9c22425be8d2112150d342e7cfb0bd4'


@app.route('/')
def home_page():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows, user=queries.get_user_by_username(session.get('username')))


@app.route('/design')
def design():
    return render_template('design.html', user=queries.get_user_by_username(session.get('username')))


@app.route('/shows')
@app.route('/shows/<sort>')
@app.route('/shows/<sort>/<order>')
def get_all_shows(sort='most-rated', order='desc'):
    page = request.args.get('page')
    if page is None or not page.isdigit():
        page = 1
    else:
        page = int(page)
    shows = queries.get_shows_sorted_by(page, sort, order)
    shows_count = queries.get_shows_count()['count']
    all_pages = math.floor((shows_count - 15) / 15)
    return render_template('shows.html',
                           order=order,
                           shows=shows,
                           page_now=page,
                           all_pages=all_pages,
                           user=queries.get_user_by_username(session.get('username')))


@app.route('/show/<id_>')
def single_show(id_):
    show = queries.get_single_show(id_)
    print(show)
    return render_template('show.html', show=show, user=queries.get_user_by_username(session.get('username')))


@app.route('/ordered-shows')
def get_ordered_shows():
    shows = queries.get_ordered_shows()
    for show in shows:
        show['rating'] = round(int(show['rating'])) * '☆'
    return render_template('ordered-shows.html', shows=shows, user=queries.get_user_by_username(session.get('username')))


@app.route('/ordered-shows', methods=['POST'])
def post_ordered_shows():
    data = request.get_json()
    print(data)
    shows = queries.get_ordered_shows(data['order'])
    return jsonify(shows)


@app.route('/year-exam')
def get_year_exam():
    actors = queries.get_actors_2010_2012()
    print("actors", actors)
    return render_template('year-exam.html', actors=actors, user=queries.get_user_by_username(session.get('username')))


@app.route('/year-exam', methods=['POST'])
def post_year_exam():
    data = request.get_json()
    print("data", data)
    actors = queries.get_actors_2010_2012(data['order'])
    return jsonify(actors)


@app.route('/filter-actors')
def get_filter_actors():
    genres = queries.get_all_genres()
    actors = queries.get_filtered_actors()
    return render_template('filter-actors.html', genres=genres, actors=actors)


@app.route('/filter-actors', methods=['POST'])
def post_filter_actors():
    data = request.get_json()
    actors = queries.get_filtered_actors(data['genre'], data['name'])
    return jsonify(actors)

#
# @app.route('/plus-4-seasons')
# def get_plus5seasons():
#     seasons = queries.get_plus_4_seasons()
#     return render_template('plus-4-seasons.html', seasons=seasons,
#                            user=queries.get_user_by_username(session.get('username')))
#
#
# @app.route('/plus-4-seasons', methods=['POST'])
# def post_plus5seasons():
#     data = request.get_json()
#     print(data)
#     seasons = queries.get_plus_4_seasons(data['phrase'])


@app.route('/register', methods=['POST'])
def post_register_page():
    user_data = request.get_json()
    print(user_data)
    username = user_data['username']
    password_1 = user_data['password']
    password_2 = user_data['password2']
    if not queries.get_user_by_username(username):
        if password_1 == password_2:
            new_user = {'username': username,
                        'password': auth.hash_password(password_1)}
            queries.add_new_user(new_user)
            session['username'] = username
            flash('Successfully Registered! You are logged in now.', category='success')
            return jsonify({'url': request.root_url}), 200
        flash("Passwords do not match!", category='error')
        return jsonify({'url': request.root_url}), 403
    flash('User already exists!', category='error')
    return jsonify({'url': request.root_url}), 409


@app.route('/login', methods=['POST'])
def post_login_page():
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']
    user = queries.get_user_by_username(username)
    if user and auth.verify_password(password, user['password']):
        session['username'] = username
        flash('Successfully logged!', category='success')
        return jsonify({'url': request.root_url}), 200
    flash('Wrong user details!', category='error')
    return jsonify({'url': request.root_url}), 401


@app.route('/logout', methods=['POST'])
def post_logout():
    session.pop('username', None)
    return redirect(url_for('home_page'))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
