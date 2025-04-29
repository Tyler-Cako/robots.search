from flask import Flask, render_template, request
from lib.funcs import DocumentSearch, Recommender
import ast

app = Flask(__name__)
search = DocumentSearch()
recommend = Recommender()

@app.get("/")
def search_page():
    return render_template("index.html", results=[])

@app.post('/')
def search_results():
    search_query = request.form['search_query']
    results = search.search(search_query, 10)

    print(request.form)

    return render_template("index.html", results=results, search_query=search_query)

@app.post('/recommendations')
def recommend_papers():
    title = request.form['title']
    url = request.form['url']
    abstract = request.form['abstract']
    tags = request.form['tags']

    selected = {
        'title': title,
        'url': url,
        'abstract': abstract,
        'tags': ast.literal_eval(tags)
    }

    selected_idx = recommend.get_index_of_url(url)

    recs = recommend.find_similar(selected_idx, 5)

    print(recs)

    return render_template("recommend.html", recs=recs, selected=selected)


if __name__ == "__main__":
    app.run(debug=True)