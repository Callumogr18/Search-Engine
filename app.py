from flask import Flask, request
from search import search
import html

app = Flask(__name__)

styles = """
<style>
    .site {
        font-size: .8rem;
        color: green;
    }
    
    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
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


