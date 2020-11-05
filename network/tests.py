from django.test import Client, TestCase
from .models import Post, User
from datetime import datetime
from django.utils import timezone
from .forms import PostForm

def createUser(username, email, password):
    u = User()
    u.username = username
    u.email = email
    u.set_password(password)
    u.save()
    return u

# Create your tests here.
class TestsPostModel(TestCase):

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

class TestIndexView(TestCase):

    def test_get_index_view(self):
        """*** Index view request needs to be with response 200 ***"""
        c = Client()
        response = c.get(f"/")
        self.assertEqual(response.status_code, 200)

class TestPostAction(TestCase):

    def test_post_action_return_302_logged_out(self):
        """*** Post action should return 302 on logged out request ***"""
        c = Client()
        response = c.post(f"/post")
        self.assertEqual(response.status_code, 302)
        response = c.get(f"/post")
        self.assertEqual(response.status_code, 302)

    def test_post_action_return_200(self):
        """*** Post action must return 200 ***"""
        u = createUser("foo", "foo@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/post")
        self.assertEqual(response.status_code, 200)

    def test_post_action_return_404_with_get_request(self):
        """*** Post action must return 404 error code on GET request ***"""
        u = createUser("foo", "foo@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/post")
        self.assertEqual(response.status_code, 404)

class TestAllPosts(TestCase):

    def test_get_all_posts(self):
        """*** Index should return 2 posts ***"""
        u = createUser("foo", "foo@example.com", "example")
        m = "New post message 1"
        p = Post()
        p.post(m, u)
        m = "New post message 2"
        p = Post()
        p.post(m, u)
        c = Client()
        response = c.get(f"/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 2)

class TestUser(TestCase):

    def test_follow(self):
        """*** Should foo follow juan, then juan followers must return foo ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        self.assertIn(foo, juan.followers.all())
        self.assertIn(juan, foo.following.all())
        self.assertNotIn(foo, juan.following.all())

class TestProfile(TestCase):

    def test_get_profile_view(self):
        """*** Profile view get request should return 200 on logged out and logged in request ***"""
        u = createUser("foo", "foo@example.com", "example")
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertEqual(response.status_code, 200)
        c.login(username='foo', password='example')
        response = c.get(f"/profile/foo")
        self.assertEqual(response.status_code, 200)

    def test_get_profile_view_post_request_not_available(self):
        """*** Profile view get request should return 404 on post request ***"""
        c = Client()
        response = c.post(f"/profile/foo")
        self.assertEqual(response.status_code, 404)

    def test_get_profile_view_post_404_when_user_not_found(self):
        """*** Profile view get request should return 404 when user is not found ***"""
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertEqual(response.status_code, 404)

    def test_get_profile_view_return_profile_html(self):
        """*** Profile view get request should return network/profile.html ***"""
        foo = createUser("foo", "foo@example.com", "example")
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertTemplateUsed(response, 'network/profile.html')

    def test_get_profile_view_context_data(self):
        """*** Profile view get request context should return user followed and following count ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        zoe = createUser("zoe", "zoe@example.com", "example")
        foo.follow(juan)
        foo.follow(zoe)
        zoe.follow(foo)
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertEqual(response.context["followingCount"], 2)
        self.assertEqual(response.context["followersCount"], 1)

if __name__ == "__main__":
    unittest.main()
