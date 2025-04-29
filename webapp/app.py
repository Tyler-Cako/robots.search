from flask import Flask, render_template, request
from lib.funcs import DocumentSearch
import ast

app = Flask(__name__)
search = DocumentSearch()

@app.get("/")
def search_page():
    return render_template("index.html", results=[])

@app.post('/results')
def search_results():
    search_query = request.form['search_query']
    results = search.search(search_query, 5)

    

    for result in results:
        tag_list = ast.literal_eval(result['tags'])
        result['tag_list'] = tag_list

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)