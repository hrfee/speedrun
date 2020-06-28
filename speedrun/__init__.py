import srcomapi
import plotly
import json
import pandas as pd
import datetime
from flask import Flask, render_template, request, jsonify
from waitress import serve

api = srcomapi.SpeedrunCom()
api.debug = 0

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    games = api.search(srcomapi.datatypes.Game, data)[:10]
    response = {"games": [g.name for g in games]}
    return jsonify(response), 200


@app.route("/categories", methods=["POST"])
def categories():
    data = request.get_json()
    game = api.search(srcomapi.datatypes.Game, data)[0]
    raw_cats = game.categories
    cats = {"categories": []}
    for cat in raw_cats:
        if cat.type == "per-game":
            cats["categories"].append(cat.name)
    return jsonify(cats)


@app.route("/graph", methods=["POST"])
def graph():
    data = request.get_json()
    game = api.search(srcomapi.datatypes.Game, {"name": data["name"]})[0]
    for cat in game.categories:
        if data["category"] == cat.name and cat.type == "per-game":
            category = cat
    release_date = datetime.datetime.strptime(game.release_date, "%Y-%m-%d")
    data = srcomapi.datatypes.Leaderboard(
        api,
        data=api.get(f"leaderboards/{game.id}/category/{category.id}?embed=variables"),
    )
    raw_runs = data.runs
    runs = {"Time": [], "Days since release": [], "Annotation": []}
    for run in raw_runs:
        r = run["run"]
        time = r.times["primary_t"]
        if r.date is not None:
            date = datetime.datetime.strptime(r.date, "%Y-%m-%d")
            time_since_release = date - release_date
            runs["Time"].append(time / 60)
            runs["Days since release"].append(time_since_release.days)
            # if len(r.players) == 1:
            #     players = r.players[0].name
            # elif len(r.players) > 1:
            #     players = ''
            #     for i, p in enumerate(r.players):
            #         players += p.name
            #         if i != len(r.players) - 1:
            #             players += ', '
            annotation = (
                # f'players: {players}\n'
                f"date: {r.date}"
            )
            runs["Annotation"].append(annotation)
    graph = plotly.graph_objs.Figure()
    trace = plotly.graph_objs.Scatter(
        x=runs["Days since release"],
        y=runs["Time"],
        mode="markers",
        hoverinfo="text",
        hovertext=runs["Annotation"],
    )
    graph.add_trace(trace)
    graph.update_layout(
        title=f"{game.name} ({category.name}): Run time since release",
        xaxis_title="Days since release",
        yaxis_title="Time (Minutes)",
    )
    graph_json = graph.to_json()
    # graph_json = json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)
    return app.response_class(
        response=graph_json, status=200, mimetype="application/json"
    )


def main():
    global app
    serve(app, host="0.0.0.0", port=8059)
