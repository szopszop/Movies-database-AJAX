from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows(page=1, rows_per_page=15):
    offset_query = 'OFFSET %(offset)s' if page > 1 else ';'
    return data_manager.execute_select("""
    SELECT shows.id, shows.title, EXTRACT(YEAR FROM shows.year) AS year,
            shows.runtime,ROUND(shows.rating, 1) AS rating,
            STRING_AGG(genres.name, ', ' ORDER BY genres.name) AS genre,
            shows.trailer, shows.homepage
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY  shows.id, shows.rating
    ORDER BY shows.rating DESC
    LIMIT """ + str(rows_per_page) + offset_query, variables={'offset': (page - 1) * rows_per_page})


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
    ORDER BY shows.rating DESC
    ;""", {'show_id': show_id}, fetchall=False)


def get_shows_count():
    return data_manager.execute_select('SELECT COUNT(*) AS count FROM shows;', fetchall=False)
