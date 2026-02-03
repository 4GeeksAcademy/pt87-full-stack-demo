"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from typing import List
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_cors import CORS
from flask_jwt_extended import (
    jwt_required, create_access_token, current_user,
)

from api.utils import generate_sitemap, APIException
from api.models import db, User, Post

api = Blueprint('api', __name__)

# Allow CORS requests to this APIf
CORS(api)


@api.route("signup", methods=["POST"])
def signup():
    user = db.session.scalars(
        db.select(User).filter_by(
            username=request.json.get("username")
        )
    ).first()

    if user:
        return jsonify(msg="Invalid username or password"), 400

    user = User(**request.json)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())


@api.route("/login", methods=["POST"])
def login():
    user = db.session.scalars(
        db.select(User).filter_by(
            username=request.json.get("username")
        )
    ).one_or_none()

    if not user:
        return jsonify(msg="Invalid username or password"), 401

    if not user.check_password_hash(request.json.get("password", "")):
        return jsonify(msg="Invalid username or password"), 401

    return (jsonify(
        token=create_access_token(identity=user)
    ))


@api.route("/changepwd", methods=["PATCH", "PUT"])
@jwt_required()
def changepwd():
    data: dict = request.json

    if not data.get("password"):
        return jsonify(msg="Invalid password."), 400

    user = current_user

    current_user.password = data.get("password")

    db.session.merge(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())


@api.route("/posts", methods=["POST"])
@jwt_required()
def create_posts():
    data: dict = request.json

    post: Post = Post(
        title=data.get("title", ""),
        content=data.get("content", ""),
        user=current_user,
    )

    db.session.add(post)
    db.session.commit()
    db.session.refresh(post)

    return jsonify(post.serialize()), 200


@api.route("/posts", methods=["GET"])
def read_posts():
    posts: List[Post] = db.session.scalars(
        db.select(Post)
        .fetch(min(100, int(request.args.get("limit", "10"))))
        .offset(int(request.args.get("offset", "0")))
        .order_by(Post.id)
    ).all()
    post_count: int = db.session.query(Post).count()
    return jsonify(
        posts=[post.serialize() for post in posts],
        total=post_count,
    )


@api.route("/posts/<int:id>", methods=["PATCH", "PUT"])
def update_posts(id: int):
    data: dict = request.json
    post: Post = db.get_or_404(Post, id)

    for key, value in data.items():
        setattr(post, key, value)

    db.session.merge(post)
    db.session.commit()
    db.session.refresh(post)

    return jsonify(post.serialize()), 200


@api.route("/posts/<int:id>", methods=["DELETE"])
def delete_posts(id: int):
    post: Post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return "", 204
