from flask import Flask, request
from search import search
import html

app = Flask(__name__)

styles = """
<style>
    body {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #ffffff;
        color: #333;
        margin: 0;
        padding: 20px;
    }

    .search-container {
        text-align: center;
        margin-bottom: 20px;
    }

    input[type="text"] {
        padding: 10px;
        width: 300px;
        border: 2px solid #ccc;
        border-radius: 5px;
    }

    input[type="submit"] {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #28a745;
        color: white;
        cursor: pointer;
        margin-left: 10px;
    }

    input[type="submit"]:hover {
        background-color: #218838;
    }

    .result {
        border-bottom: 1px solid #eaeaea;
        padding: 10px 0;
    }

    .site {
        font-weight: bold;
        color: #007bff;
    }

    .snippet {
        font-size: 0.9rem;
        color: #666;
    }
</style>
"""

search_template = styles + """
<form action="/" method="POST">
    <input type="text" name="query">
    <input type="submit" name="Search">    
</form>
"""

result_template = """
<p class="site">{rank}: {link}</p>
<a href="{link}>{title}</a>
<p class="snippet">{snippet}</p>
"""

def show_search_form():
    return search_template

def run_search(query):
    results = search(query)
    rendered = search_template
    results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))
    for index, row in results.iterrows():
        rendered += result_template.format(**row)
    return rendered

@app.route('/', methods = ['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()


