from app import *

@app.route('/api/v1/users/', methods=["GET", "POST"])
def index_user():
    if request.method == "GET":
        users = session.query(User).all()
        return ConnectedUserSchema(many=True).dump(users)
    if request.method == "POST":
        name = request.json.get('name', '')
        display_email = request.json.get('display_email', '')
        picture_url = request.json.get('picture_url', '')
        about = request.json.get('about', '')
        zipcode = request.json.get('zipcode', '')
        user = User(name=name, display_email=display_email, picture_url=picture_url, about=about, zipcode=zipcode)
        db.session.add(user)
        #db.session.commit()
        return UserSchema().dump(user)

@app.route('/api/v1/users/<int:user_id>/', methods=["GET", "DELETE", "PATCH"])
def show_user(user_id):
    if request.method == "GET":
        user = db.session.get(User, user_id)
        return UserSchema().dump(user)

    if request.method == "DELETE":
        user = db.session.get(User, user_id)
        db.session.delete(user)
        #db.session.commit()
        return "User successfully deleted"

    if request.method == "PATCH":
        user = db.session.get(User, user_id)
        body = request.get_json()
        if 'name' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(name=body['name']))
            #db.session.commit()
        if 'display_email' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(display_email=body['display_email']))
            #db.session.commit()
        if 'picture_url' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(picture_url=body['picture_url']))
            #db.session.commit()
        if 'about' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(about=body['about']))
            #db.session.commit()
        if 'zipcode' in body:
            db.session.query(User).filter_by(id=user_id).update(dict(zipcode=body['zipcode']))
            #db.session.commit()
        if 'instrument' in body:
            instrument = db.session.query(Instrument).filter_by(name=body['instrument']).first()
            if len(session.query(user_instrument).filter_by(user_id=user_id, instrument_id=instrument.id).all()) == 0:
                ins = user_instrument.insert().values(user_id=user_id, instrument_id=instrument.id)
                db.engine.execute(ins)
                #db.session.commit()
        if 'genre' in body:
            genre = db.session.query(Genre).filter_by(name=body['genre']).first()
            if len(session.query(user_genre).filter_by(user_id=user_id, genre_id=genre.id).all()) == 0:
                ins = user_genre.insert().values(user_id=user_id, genre_id=genre.id)
                db.engine.execute(ins)
                #db.session.commit()

        return UserSchema().dump(user)

@app.route('/api/v1/users/<int:user_id>/connections/')
def show_user_connections(user_id):
    user = db.session.get(User, user_id)
    return UserConnectionsSchema().dump(user)

@app.route('/api/v1/instruments/', methods=['POST'])
def create_instrument():
    name = request.json.get('name', '')
    instrument = Instrument(name=name)
    needs_instrument = NeedsInstrument(name=name)
    db.session.add(instrument)
    db.session.add(needs_instrument)
    #db.session.commit()
    return instrument_schema.jsonify(instrument)

@app.route('/api/v1/genres/', methods=['POST'])
def create_genre():
    name = request.json.get('name', '')
    genre = Genre(name=name)

    db.session.add(genre)
    #db.session.commit()
    return genre_schema.jsonify(genre)

@app.route('/api/v1/users/<int:user_id>/instruments/<int:instrument_id>/', methods=['POST'])
def create_user_instrument(user_id, instrument_id):
    ins = user_instrument.insert().values(user_id=user_id, instrument_id=instrument_id)
    db.engine.execute(ins)
    #db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/needs_instruments/<int:needs_instrument_id>/', methods=['POST'])
def create_user_needs_instrument(user_id, needs_instrument_id):
    ins = user_needs_instrument.insert().values(user_id=user_id, needs_instrument_id=needs_instrument_id)
    db.engine.execute(ins)
    #db.session.commit()
    return "connection added"

@app.route('/api/v1/users/<int:user_id>/genres/<int:genre_id>/', methods=['POST'])
def create_user_genre(user_id, genre_id):
    ins = user_genre.insert().values(user_id=user_id, genre_id=genre_id)
    db.engine.execute(ins)
    #db.session.commit()
    return "connection added"



    if request.method == "DELETE":
        user = db.session.get(User, user_id)
        db.session.delete(user)
        #db.session.commit()
        return "User successfully deleted"

@app.route('/api/v1/users/<int:user_id>/connections/<int:friend_id>/', methods=['POST', 'PATCH', 'DELETE'])
def crud_user_connection(user_id, friend_id):

    if request.method == 'POST':
        ins = user_connection.insert().values(user_id=user_id, friend_id=friend_id, status='PENDING')
        db.engine.execute(ins)
        #db.session.commit()
        return "connection added"

    if request.method == 'PATCH':
        status_input = request.json.get('status', '')
        u = connections_table.update()
        u = u.values({"status": status_input})
        if len(session.query(user_connection).filter_by(friend_id = friend_id, user_id = user_id).all()) == 1:
            u = u.where(connections_table.c.user_id == user_id, connections_table.c.friend_id == friend_id)
        elif len(session.query(user_connection).filter_by(friend_id = user_id, user_id = friend_id).all()) == 1:
            u = u.where(connections_table.c.user_id == friend_id, connections_table.c.friend_id == user_id)
        else:
            return "no connection pending"
        engine.execute(u)
        return {"response": "connection updated"}

    if request.method == 'DELETE':
        u = connections_table.delete()
        u = u.where(connections_table.c.user_id == user_id, connections_table.c.friend_id == friend_id)
        engine.execute(u)
        return "connection deleted"

@app.route('/api/v1/users/<int:user_id>/instruments/', methods=['GET'])
def get_user_instruments(user_id):
    user = db.session.get(User, user_id)
    return InstrumentSchema(many=True).dump(user.instruments)

def zip_distance(zip1, zip2):
    dist = pgeocode.GeoDistance('us')
    return dist.query_postal_code(zip1, zip2)

@app.route('/api/v1/users/<int:user_id>/search/', methods=['GET'])
def get_user_search(user_id):
    name_query = ''
    genre_query = ''
    instrument_query = ''
    distance_query = 100

    if 'name' in request.args:
        name_query = request.args.get("name")
    if 'instrument' in request.args:
        instrument_query = request.args.get("instrument")
    if 'genre' in request.args:
        genre_query = request.args.get("genre")
    if 'distance' in request.args:
        distance_query = request.args.get("distance")
    # user = db.session.get(User, user_id)
    users = session.query(User) \
        .filter(User.name.ilike(f'%{name_query}%')) \
        .join(User.instruments) \
        .filter(Instrument.name.ilike(f'%{instrument_query}%')) \
        .join(User.genres) \
        .filter(Genre.name.ilike(f'%{genre_query}%')) \
        .order_by(User.name) \
        .all()

    # zip_hash = {}
    # for i in users:
    #     zip_hash[i.id] = zip_distance(i.zipcode, user.zipcode)
    # for k, v in list(zip_hash.items()):
    #     if zip_hash[k] > int(distance_query):
    #         del zip_hash[k]
    # zip_hash = dict(sorted(zip_hash.items(), key=lambda x:x[1]))

    # users = []
    # for k, v in list(zip_hash.items()):
    #     users.append(User.query.get(k))

    response = UserSchema(many=True, exclude = ('display_email', 'zipcode')).dump(users)
    # for i in response['data']:
    #     # i['attributes']['distance'] = zip_hash[int(i['id'])]
    #     if len(session.query(user_connection).filter_by(status = 'APPROVED', friend_id = int(i['id']), user_id = user.id).all()) == 1 \
    #     or len(session.query(user_connection).filter_by(status = 'APPROVED', user_id = int(i['id']), friend_id = user.id).all()) == 1:
    #         i['attributes']['connection_status'] = 'approved'
    #     elif len(session.query(user_connection).filter_by(status = 'PENDING', friend_id = int(i['id']), user_id = user.id).all()) == 1 \
    #     or len(session.query(user_connection).filter_by(status = 'PENDING', user_id = int(i['id']), friend_id = user.id).all()) == 1:
    #         i['attributes']['connection_status'] = 'pending'
    #     elif len(session.query(user_connection).filter_by(status = 'REJECTED', friend_id = int(i['id']), user_id = user.id).all()) == 1 \
    #     or len(session.query(user_connection).filter_by(status = 'REJECTED', user_id = int(i['id']), friend_id = user.id).all()) == 1:
    #         i['attributes']['connection_status'] = 'rejected'
    #     else:
    #         i['attributes']['connection_status'] = 'nun'

    return response
