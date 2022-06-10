from flask import Flask, render_template, redirect, request

app = Flask(__name__, template_folder='templates/')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        game = request.form["game"]
        skill = request.form["skill"]
        behaviour = request.form["behaviour"]
        granularity = request.form["granularity"]

        # print(game, skill, behaviour, granularity)
        return redirect(
            f"http://localhost:8002/play_game?game={game}&skill={skill}&behaviour={behaviour}&granularity={granularity}&return=http://localhost:8003/match")

    return render_template('index.html')


@app.route("/match", methods=["GET"])
def match():
    return render_template("match.html", results=request.args.get("results"),
                           reputation=request.args.get("reputation"),
                           behaviour=request.args.get("behaviour"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
