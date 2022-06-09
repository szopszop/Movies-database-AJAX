from flask import Flask, render_template, url_for, redirect, request
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated')
def most_rated():
    rows_per_page = 10
    page = request.args.get('page')
    if page is None or not page.isdigit():
        page = 1
    else:
        page = int(page)
    highest_rated_shows = queries.get_most_rated_shows(page, rows_per_page)
    shows_count = queries.get_shows_count()['count']
    return render_template('most-rated.html', shows=highest_rated_shows, page_now=page,
                           pages=math.floor((shows_count - rows_per_page) / rows_per_page))


@app.route('/show/<id_>')
def single_show(id_):
    show = queries.get_single_show(id_)
    print(show)
    return render_template('single-show.html', show=show)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
