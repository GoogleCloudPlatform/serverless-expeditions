from flask import Flask, render_template
from pathlib import Path
import jinja2
import frontmatter
import markdown2
import os

app = Flask(__name__, static_url_path='', static_folder='media')

ENTRIES_DIR = "_entries"
ENTRY_PATH = "/entry/"


def markdown(text):
    return markdown2.markdown(text)

app.add_template_filter(markdown)



def get_entries():
    entries = []
    path = Path(ENTRIES_DIR).glob("*.md")
    for f in path:
        entry = frontmatter.load(f)
        entry['url'] = ENTRY_PATH + Path(f).stem
        entries.append(entry)
    return entries
    

@app.route("/entry/<title>")
def entry(title):
    f = Path(ENTRIES_DIR, f"{title}.md")
    if f.exists():
        return render_template("entry.html", entry=frontmatter.load(f))
    else:
        return render_template("404.html")

@app.route("/")
def home():
    entries = get_entries()
    return render_template("home.html", entries=entries)


if __name__ == "__main__":
    app.run() #, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))