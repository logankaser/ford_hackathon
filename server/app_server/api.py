

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for, Response, current_app, send_file
)


@bp.route("/search/<keyword>", methods="GET")
def search(keyword):
    results = Post.query.msearch(keyword, fields=["name", "description"],
                                 limit=10)
    