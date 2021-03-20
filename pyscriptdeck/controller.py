import json
from flask import Flask, request, abort, jsonify, render_template
from flask import redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException
from pyscriptdeck.config import getconfig
from pyscriptdeck.main import Main


def init_app(app: Flask, main: Main):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/info")
    def info():
        return render_template("info.html", status=main.get_status())

    @app.route("/history")
    def history():
        return render_template("history.html")

    @app.route("/script/<script_id>")
    def script(script_id=None):
        check_script_id(script_id)
        return render_template("script.html", script_id=script_id)

    def check_script_id(script_id):
        if script_id is None:
            abort(400, "script_id is None")
        if not main.is_script_exist(script_id):
            abort(404, "script not found for id '{}'".format(script_id))

    @app.route("/api/scripts")
    def api_get_scripts():
        return jsonify(main.get_scripts_descriptions())

    @app.route("/api/scripts/<script_id>")
    def api_get_script(script_id=None):
        check_script_id(script_id)
        return main.get_script_info(script_id)

    @app.route("/api/scripts/<script_id>/executions")
    def api_get_script_executions(script_id=None):
        check_script_id(script_id)
        return jsonify(main.get_script_executions(script_id))

    @app.route("/api/scripts/<script_id>/_run", methods=["POST"])
    def api_run_scripts(script_id=None):
        check_script_id(script_id)
        return main.run_script(script_id, request.json)

    @app.route("/api/executions")
    def api_get_executions():
        return jsonify(main.get_executions())

    @app.route("/api/groups")
    def api_get_groups():
        return jsonify(main.get_groups())

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            login_result = main.login(request.form["login"], request.form["password"])
            if login_result:
                session["user"] = request.form["login"]
                flash("You have successfully logged in")
                return redirect(url_for("index"))
            error = "Invalid credentials"

        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("You have been successfully logged out")
        return redirect(url_for("index"))

    @app.route("/api/status")
    def api_status():
        return main.get_status()

    @app.context_processor
    def inject_global():
        config = getconfig()
        app_demo = "app.demo" in config and config["app.demo"]
        return {
            "app_title": config["app.title"],
            "app_demo": app_demo
        }

    @app.before_request
    def check_authentication():
        if "user" not in session and request.path != "/api/status":
            if request.path.startswith("/api"):
                abort(401)
            elif (not request.path.startswith("/login")
                  and not request.path.startswith("/static")):
                return redirect(url_for("login"))

    @app.errorhandler(HTTPException)
    def handle_http_exception(exception):
        response = exception.get_response()
        if not request.path.startswith("/api"):
            return response

        response.data = json.dumps({
            "code": exception.code,
            "name": exception.name,
            "description": exception.description,
        })
        response.content_type = "application/json"
        return response

    def to_pretty_json(value):
        return json.dumps(value, sort_keys=True, indent=4, separators=(',', ': '))

    app.jinja_env.filters['tojson_pretty'] = to_pretty_json
