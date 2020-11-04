from django.test import TestCase
from .models import Post, User
from datetime import datetime
from django.utils import timezone

def createUser(username, email, password):
    u = User()
    u.username = username
    u.email = email
    u.password = password
    u.save()
    return u

# Create your tests here.
class TestsPost(TestCase):

    def test_get_post_message(self):
        """*** Printing the post needs to be equal to the post message ***"""
        u = createUser("foo", "foo@example.com", "exmaple")
        m = "New post message"
        p = Post()
        p.post(m, u)
        self.assertEqual(str(p), m)

    def test_get_post_user(self):
        """*** Post needs to be posted by a User ***"""
        u = createUser("foo", "foo@example.com", "exmaple")
        m = "New post message"
        p = Post()
        p.post(m, u)
        self.assertEqual(p.user, u)

    def test_get_post_timestamp(self):
        """*** Post needs to be timestamped ***"""
        u = createUser("foo", "foo@example.com", "exmaple")
        m = "New post message"
        p = Post()
        p.post(m, u)
        p.save()
        self.assertTrue(abs(p.created_at - timezone.now()) < timezone.timedelta(seconds=5))

if __name__ == "__main__":
    unittest.main()
