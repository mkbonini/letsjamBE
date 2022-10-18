# app/routes.py

from app import app
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
#
# @app.route('/users/<int:user_id>/')
# def show_user(user_id):
#     user = User.query.get(user_id)
#     return user_schema.jsonify(user)
#
# @app.route('/users/', methods=['POST'])
# def create_user():
#     name = request.json.get('name', '')
#     display_email = request.json.get('display_email', '')
#     picture_url = request.json.get('picture_url', '')
#     about = request.json.get('about', '')
#     zipcode = request.json.get('zipcode', '')
#     user = User(name=name, display_email=display_email, picture_url=picture_url, about=about, zipcode=zipcode)
#
#     db.session.add(user)
#     db.session.commit()
#     return user_schema.jsonify(user)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
