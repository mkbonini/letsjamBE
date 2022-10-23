from app import app, User
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

