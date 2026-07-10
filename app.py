from flask import Flask, render_template, request
from agents import run_study_mentor
import markdown


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":
        question = request.form["question"]

        answer = markdown.markdown(
    run_study_mentor(question),
    extensions=["extra"]
)

    return render_template(
        "index.html",
        answer=answer
    )


if __name__ == "__main__":
    app.run(debug=True)
