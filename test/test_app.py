from app import app, User, Instrument, NeedsInstrument, Genre
import pytest

def test_always_passes():
    assert True

def test_new_user():
    user = User('Bory Cethune', 'bcethune@email.com', 'www.pictureofmyself.com', 'I want to jam!', '80000')
    assert user.name == 'Bory Cethune'
    assert user.display_email == 'bcethune@email.com'
    assert user.picture_url == 'www.pictureofmyself.com'
    assert user.about == 'I want to jam!'
    assert user.zipcode == '80000'


def test_new_instrument():
    instrument = Instrument('Clarinet')
    assert instrument.name == 'Clarinet'


def test_needs_instrument():
    needs_instrument = NeedsInstrument('Piano')
    assert needs_instrument.name == 'Piano'

# class NeedsInstrument(db.Model):
#     __tablename__ = "needs_instrument"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#    class Instrument(db.Model):
#     __tablename__ = "instrument"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

