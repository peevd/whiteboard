from . import auth
from ... import db
from ...models.users import User

from datetime import datetime, timedelta
# import os
import jwt
import json
import requests
from urllib.parse import parse_qsl
from flask import request, jsonify
from flask import current_app as app

# import base64
# from functools import wraps
# from urllib.parse import parse_qs, parse_qsl, urlencode
# from jwt import DecodeError, ExpiredSignature
# url_for, redirect, Flask, g, send_file,


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


@auth.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,photos'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)
    # print(json.dumps(profile, indent=2))

    # print(json.dumps(token, indent=4))
    # print("******************************************************")
    # Step 4. Create a new account or return an existing one.
    # print(json.dumps(profile, indent=4))
    admin_moderator_check = User.query.filter_by(email=profile["emailAddresses"][0]["value"]).first()
    if admin_moderator_check and admin_moderator_check.role_id in [1, 2]:
        admin_moderator_check.first_name = profile["names"][0]["givenName"]
        admin_moderator_check.last_name = profile["names"][0]["familyName"]
        admin_moderator_check.google = profile["names"][0]["metadata"]["source"]["id"]
        admin_moderator_check.picture = profile["photos"][0]["url"]

        db.session.commit()
        token = create_token(admin_moderator_check)
        # print(token)
        # print("_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|")
        return jsonify(token=token)

    user = User.query.filter_by(google=profile["names"][0]["metadata"]["source"]["id"]).first()
    if user:
        if user.picture != profile["photos"][0]["url"]:
            user.picture = profile["photos"][0]["url"]
            db.session.commit()

        token = create_token(user)
        # print(token)
        # print("_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|")
        return jsonify(token=token)

    u = User(first_name=profile["names"][0]["givenName"],
             last_name=profile["names"][0]["familyName"],
             email=profile["emailAddresses"][0]["value"],
             google=profile["names"][0]["metadata"]["source"]["id"],
             picture=profile["photos"][0]["url"])

    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    # print(token)
    # print("_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|")
    return jsonify(token=token)


@auth.route('/auth/facebook', methods=['POST'])
def facebook():
    access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.3/me'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': app.config['FACEBOOK_SECRET'],
        'code': request.json['code']
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.get(access_token_url, params=params)
    access_token = dict(parse_qsl(r.text))

    # Step 2. Retrieve information about the current user.
    r = requests.get(graph_api_url, params=access_token)
    profile = json.loads(r.text)

    # Step 4. Create a new account or return an existing one.
    user = User.query.filter_by(facebook=profile['id']).first()
    if user:
        token = create_token(user)
        return jsonify(token=token)

    u = User(facebook=profile['id'], display_name=profile['name'])
    db.session.add(u)
    db.session.commit()
    token = create_token(u)
    return jsonify(token=token)

