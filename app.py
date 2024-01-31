
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from recommender import Recommender

recommender = Recommender()
@app.route('/', methods=['GET', 'POST'])
def recommend():
    data: list[list[str]] = [[]]
    if request.method == "POST":
        book_name = request.form.get('book_name')
        pt = recommender.recommend(book_name)
        return render_template('index.html', data=pt)
    else:
        return render_template('index.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
