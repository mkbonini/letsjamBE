from app import *

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    display_email = fields.Str()
    about = fields.Str()
    zipcode = fields.Str()
    picture_url = fields.Str()
    instruments = fields.Nested(lambda: InstrumentSchema(only=("name","id"), many=True))
    needs_instruments = fields.Nested(lambda: NeedsInstrumentSchema(only=("name","id"), many=True))
    genres = fields.Nested(lambda: GenreSchema(only=("name","id"), many=True))

    class Meta:
        type_ = "user"
        strict = True
        ordered = True

class ConnectedUserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    display_email = fields.Str()
    about = fields.Str()
    zipcode = fields.Str()
    picture_url = fields.Str()
    instruments = fields.Nested(lambda: InstrumentSchema(only=("name","id"), many=True))
    needs_instruments = fields.Nested(lambda: NeedsInstrumentSchema(only=("name","id"), many=True))
    genres = fields.Nested(lambda: GenreSchema(only=("name","id"), many=True))

    class Meta:
        type_ = "user"
        strict = True
        ordered = True

class RequestedUserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    about = fields.Str()
    picture_url = fields.Str()
    instruments = fields.Nested(lambda: InstrumentSchema(only=("name","id"), many=True))
    needs_instruments = fields.Nested(lambda: NeedsInstrumentSchema(only=("name","id"), many=True))
    genres = fields.Nested(lambda: GenreSchema(only=("name","id"), many=True))

    class Meta:
        type_ = "user"
        strict = True
        ordered = True

class UserConnectionsSchema(Schema):
    id = fields.Str(dump_only=True)
    connections_pending = fields.Method("get_connections_pending")
    requests_pending = fields.Method("get_requests_pending")
    connections = fields.Method("get_connections")

    def get_connections_pending(self, user):
        pending_connections = []
        connection_list = session.query(user_connection).filter_by(status = 'PENDING', user_id = user.id).all()
        for conns in connection_list:
            pending_connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
        return RequestedUserSchema(many=True).dump(pending_connections)

    def get_connections(self, user):
        connections = []
        connection_list = session.query(user_connection).filter_by(status = 'APPROVED', user_id = user.id).all()
        for conns in connection_list:
            connections.append( session.query(User).filter_by(id=conns.friend_id).all()[0] )
        connection_list = session.query(user_connection).filter_by(status = 'APPROVED', friend_id = user.id).all()
        for conns in connection_list:
            connections.append( session.query(User).filter_by(id=conns.user_id).all()[0] )
        return ConnectedUserSchema(many=True).dump(connections)

    def get_requests_pending(self, user):
        pending_requests = []
        connection_list = session.query(user_connection).filter_by(status = 'PENDING', friend_id = user.id).all()
        for conns in connection_list:
            pending_requests.append( session.query(User).filter_by(id=conns.user_id).all()[0] )
        return RequestedUserSchema(many=True).dump(pending_requests)
    class Meta:
        type_ = "user"
        strict = True
        ordered = True

class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    class Meta:
        type_ = "instrument"

class NeedsInstrumentSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    class Meta:
        type_ = "needs_instrument"

instrument_schema = InstrumentSchema()
instruments_schema = InstrumentSchema(many=True)

# class UserInstrumentSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         table = user_instrument

# user_instrument_schema = UserInstrumentSchema()

class GenreSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

    class Meta:
        type_ = "genre"

# genre_schema = GenreSchema()
# genres_schema = GenreSchema(many=True)