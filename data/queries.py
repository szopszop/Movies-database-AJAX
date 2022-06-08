from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_single_show(show_id):
    return data_manager.execute_select("""
    SELECT shows.id, shows.title, EXTRACT(YEAR FROM shows.year) AS year,
    shows.runtime,ROUND(shows.rating, 1) AS rating,
    STRING_AGG(genres.name, ', ' ORDER BY genres.name) AS genre,
    shows.trailer, shows.homepage
    FROM shows
    JOIN show_genres ON shows.id = show_genres.show_id
    JOIN genres ON show_genres.genre_id = genres.id
    WHERE show_id = %(show_id)s
    GROUP BY  shows.id, shows.rating
    ORDER BY shows.rating DESC
    ;""", show_id, fetchall=False)


def get_most_rated_shows():
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
    LIMIT 15
    ;""")
