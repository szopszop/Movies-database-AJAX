from data import data_manager
from data import database_common

def get_table_header(sorted_by):
    match sorted_by:
        case 'most-rated':
            return 'rating'
        case 'title':
            return 'title'
        case 'year':
            return 'year'
        case 'runtime':
            return 'runtime'
        case _:
            return 'rating'


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_shows_sorted_by(page=1, sorted_by='most-rated', sort_direction='desc'):
    sorted_by = get_table_header(sorted_by)
    sort_direction = ' DESC' if sort_direction == 'desc' else ' ASC'
    offset_query = ' OFFSET %(offset)s;' if page > 1 else ';'
    return data_manager.execute_select("""
    SELECT shows.id, shows.title, EXTRACT(YEAR FROM shows.year) AS year,
            shows.runtime,ROUND(shows.rating, 1) AS rating,
            STRING_AGG(genres.name, ', ' ORDER BY genres.name) AS genre,
            shows.trailer, shows.homepage
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY  shows.id
    ORDER BY shows.""" + sorted_by + sort_direction + ' LIMIT 15' + offset_query, variables={'offset': (page - 1) * 15})


def get_single_show(show_id):
    return data_manager.execute_select("""
    SELECT shows.id, shows.title,
            TO_CHAR(shows.year, 'dd-Month-YYYY') AS date,
            shows.runtime,ROUND(shows.rating, 1) AS rating,
            STRING_AGG(DISTINCT genres.name, ', ' ORDER BY genres.name) AS genre,
            shows.trailer, shows.homepage,
            STRING_AGG(DISTINCT seasons.overview, ' ') AS overview
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    JOIN show_characters ON shows.id = show_characters.show_id
    JOIN actors ON show_characters.actor_id = actors.id
    JOIN seasons ON shows.id = seasons.show_id
    JOIN episodes ON seasons.id = episodes.season_id
    WHERE shows.id = %(show_id)s
    GROUP BY  shows.id, shows.rating, seasons.show_id
    ORDER BY shows.rating DESC;""", variables={'show_id': show_id}, fetchall=False)


def get_shows_count():
    return data_manager.execute_select(
        'SELECT COUNT(*) AS count FROM shows;', fetchall=False)


@database_common.connection_handler
def get_user_by_username(cursor, username):
    query = """SELECT *
        FROM users
        WHERE username = %(username)s
        """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@database_common.connection_handler
def add_new_user(cursor, new_user):
    query = """INSERT INTO users(username, password)
            VALUES(%(username)s, %(password)s)
            """
    cursor.execute(query, {'username': new_user['username'], 'password': new_user['password']})


def get_ordered_shows(order='desc'):
    order = 'DESC' if order == 'desc' else 'ASC'
    return data_manager.execute_select(
        """SELECT shows.title,
            ROUND(shows.rating, 1) AS rating,
            COUNT(episodes.id) AS episodes_count
        FROM shows
        JOIN seasons on shows.id = seasons.show_id
        JOIN episodes on seasons.id = episodes.season_id
        GROUP BY shows.title, shows.rating
        ORDER BY episodes_count """ + order + " LIMIT 10")


def get_actors_2010_2012(order='desc'):
    order = 'DESC' if order == 'desc' else 'ASC'
    return data_manager.execute_select(
        """SELECT actors.id, actors.name , EXTRACT(YEAR FROM actors.death) AS date,
        STRING_AGG(DISTINCT show_characters.character_name, ', ' ORDER BY show_characters.character_name) AS character
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        JOIN show_characters ON shows.id = show_characters.show_id
        JOIN actors ON show_characters.actor_id = actors.id
        JOIN seasons ON shows.id = seasons.show_id
        JOIN episodes ON seasons.id = episodes.season_id
        WHERE date_part('year', actors.death) >= 2010 and date_part('year', actors.death) <= 2012
        GROUP BY actors.id, show_characters.character_name
        ORDER BY show_characters.character_name """ + order)


def get_plus_4_seasons(phrase=''):

    return data_manager.execute_select(
        """SELECT shows.title,
           shows.year,
           shows.trailer,
           COUNT(seasons.show_id) AS number_of_seasons
        FROM shows
        JOIN seasons ON shows.id = seasons.show_id
        GROUP BY shows.title, shows.year, shows.trailer
        HAVING COUNT(seasons.show_id) >= 4
        """)

