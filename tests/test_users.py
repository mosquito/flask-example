import uuid
import string
from random import choice
from xml.etree.ElementTree import fromstring
from . import BaseTestCase, app, models


def get_random_string(length):
    return "".join(
        choice(string.ascii_letters) for _ in range(length)
    )


class UserTestCase(BaseTestCase):
    def get_data(self):
        return (
            str(uuid.uuid4()),
            "{}@{}.{}".format(
                get_random_string(5),
                get_random_string(5),
                get_random_string(3),
            ).lower()
        )

    def test_user_get(self):
        name, email = self.get_data()

        user = models.users.User(name=name, email=email)

        app.db.add(user)
        app.db.commit()

        rv = self.app.get('/users/')
        data = rv.data.decode()

        assert user.email in data
        assert user.name in data

    def test_user_post(self):
        name, email = self.get_data()

        rv = self.app.post(
            '/users/',
            data=dict(name=name, email=email),
            follow_redirects=True
        )

        data = rv.data.decode()

        assert email in data
        assert name in data
