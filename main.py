from flask import abort, Flask, redirect, render_template, request

from utils import (
    build_types,
    get_build_type,
    get_platform,
    platforms,
    get_revision,
    get_platform_string,
)

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/dl/<platform_name>")
def dl(platform_name):
    build_type = request.args.get("type")
    platform = get_platform(platform_name)
    if not platform:
        return redirect("https://www.youtube.com/embed/o_asQwJqWCI?t=16&autoplay=1")

    return redirect(platform.get_last_build_url(build_type))


@app.get("/rev/<platform_name>")
def revision(platform_name):
    build_type = request.args.get("type", "")
    platform = get_platform_string(platform_name, request)
    data = get_revision(platform, build_type)
    if data and data["content"]:
        return data
    else:
        abort(404)


@app.get("/")
def index():
    build_type_name = request.args.get("type", "")
    build_type = get_build_type(build_type_name)
    platform_name = request.args.get("platform", "")
    platform = get_platform_string(platform_name, request)

    return render_template(
        "index.html",
        build_type=build_type,
        build_types=build_types,
        platform=platform,
        platforms=platforms,
    )


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
