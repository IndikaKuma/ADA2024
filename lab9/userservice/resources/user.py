from flask import jsonify, make_response

from daos.user_dao import UserDAO
from db import Session
from jwtutil import encode_auth_token, decode_auth_token


# see https://realpython.com/token-based-authentication-with-flask/

class User:

    @staticmethod
    def create(post_data):
        session = Session()
        # check if user already exists
        user = session.query(UserDAO).filter(UserDAO.id == post_data.get('email')).first()
        if not user:
            try:
                user = UserDAO(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                session.add(user)
                session.commit()
                # generate the auth token
                auth_token = encode_auth_token(user.id)
                res = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                session.close()
                return make_response(jsonify(res)), 200
            except Exception as e:
                print(e)
                res = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(res)), 401
        else:
            res = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(res)), 202

    @staticmethod
    def get(auth_header):
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                session = Session()
                # check if user already exists
                user = session.query(UserDAO).filter(UserDAO.id == resp).first()
                res = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                session.close()
                return make_response(jsonify(res)), 200
            res = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(res)), 401
        else:
            res = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(res)), 401
