import os

from flask import Flask
from flask import render_template, request
from currency_converter import CurrencyConverter

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/", methods=["POST"])
def my_form_post():
    c = CurrencyConverter()

    euros = request.form["euros"]
    usd = round(c.convert(euros, "EUR", "USD"), 2)

    return render_template("form.html", euros=euros, usd=usd)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

