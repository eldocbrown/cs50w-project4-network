from django.test import Client, TestCase
from .models import Post, User
from datetime import datetime
from django.utils import timezone
from .forms import PostForm
import json

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

    def test_model_post_serialize(self):
        """*** Should a post be created, then can be serialized ***"""
        u = createUser("foo", "foo@example.com", "example")
        m = "New post message 1"
        p = Post()
        p.post(m, u)
        self.assertJSONEqual("{\"message\": \"New post message 1\",\"user\": {\"username\": \"foo\"}, \"created_at\": \"" + datetime.now().strftime("%b %-d %Y, %-I:%M %p") + "\"}", p.serialize())

class TestUserModel(TestCase):

    def test_follow(self):
        """*** Should foo follow juan, then juan followers must return foo ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        self.assertIn(foo, juan.followers.all())
        self.assertIn(juan, foo.following.all())
        self.assertNotIn(foo, juan.following.all())

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

    def test_get_profile_view_context_data_posts(self):
        """*** Profile view get request context should return posts in reverse chronological order ***"""
        foo = createUser("foo", "foo@example.com", "example")
        p = Post()
        p.post("First post", foo)
        p = Post()
        p.post("Second post", foo)
        p = Post()
        p.post("Last post", foo)
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertEqual(response.context["userPosts"].count(), 3)
        self.assertEqual(response.context["userPosts"][2].message, "First post")
        self.assertEqual(response.context["userPosts"][1].message, "Second post")
        self.assertEqual(response.context["userPosts"][0].message, "Last post")

    def test_get_profile_view_context_data(self):
        """*** Profile view get request context should return username ***"""
        foo = createUser("foo", "foo@example.com", "example")
        c = Client()
        response = c.get(f"/profile/foo")
        self.assertEqual(response.context["usernamestr"], "foo")

    def test_get_profile_view_context_data(self):
        """*** Profile view get request context should return following flag true if user is followed ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        zoe = createUser("zoe", "zoe@example.com", "example")
        foo.follow(juan)
        foo.follow(zoe)
        zoe.follow(foo)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/profile/zoe")
        self.assertTrue(response.context["following"])
        c.logout()
        c.login(username='zoe', password='example')
        response = c.get(f"/profile/juan")
        self.assertFalse(response.context["following"])

class TestFollow(TestCase):

    def test_follow_ok(self):
        """*** Should a user follow another user, return response 200 on posting follow/<str:usernamestr> ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/follow/juan")
        self.assertEqual(response.status_code, 200)

    def test_follow_dont_allow_get_request(self):
        """*** Should a user follow another user via GET or PUT, return 404 response ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/follow/juan")
        self.assertEqual(response.status_code, 404)
        response = c.put(f"/follow/juan")
        self.assertEqual(response.status_code, 404)

    def test_follow_return_302_logged_out(self):
        """*** Follow action should return 302 on logged out request ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        c = Client()
        response = c.post(f"/follow/juan")
        self.assertEqual(response.status_code, 302)

    def test_follow_return_404_when_user_not_found(self):
        """*** Follow request should return 404 when user is not found ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/follow/zoe")
        self.assertEqual(response.status_code, 404)

    def test_follow_cant_follow_myself(self):
        """*** Should I follow myself, then return 404 ***"""
        foo = createUser("foo", "foo@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/follow/foo")
        self.assertEqual(response.status_code, 404)

    def test_follow_cant_follow_again(self):
        """*** Should I follow a user that I am already following, then return 404 ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/follow/juan")
        response = c.post(f"/follow/juan")
        self.assertEqual(response.status_code, 404)

class TestUnfollow(TestCase):

    def test_follow_ok(self):
        """*** Should a user unfollow another user, return response 200 on posting unfollow/<str:usernamestr> ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/unfollow/juan")
        self.assertEqual(response.status_code, 200)

    def test_unfollow_allow_only_post_request(self):
        """*** Should a user unfollow another user via GET or PUT, return 404 response ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/unfollow/juan")
        self.assertEqual(response.status_code, 404)
        response = c.put(f"/unfollow/juan")
        self.assertEqual(response.status_code, 404)

    def test_unfollow_return_302_logged_out(self):
        """*** Unfollow action should return 302 on logged out request ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        c = Client()
        response = c.post(f"/unfollow/juan")
        self.assertEqual(response.status_code, 302)

    def test_unfollow_cant_unfollow_myself(self):
        """*** Should I unfollow myself, then return 404 ***"""
        foo = createUser("foo", "foo@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/unfollow/foo")
        self.assertEqual(response.status_code, 404)

    def test_unfollow_return_404_when_user_not_found(self):
        """*** Unfollow request should return 404 when user is not found ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/unfollow/zoe")
        self.assertEqual(response.status_code, 404)

    def test_unfollow_cant_unfollow_again(self):
        """*** Should I unfollow a user that I am not already following, then return 404 ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        c = Client()
        c.login(username='foo', password='example')
        response = c.post(f"/unfollow/juan")
        response = c.post(f"/unfollow/juan")
        self.assertEqual(response.status_code, 404)

class TestPostsRequest(TestCase):

    allowedFilters = ["all", "following"]

    def test_posts_filter_all_return_200(self):
        """*** Should I GET /posts/all, return 200 ***"""
        c = Client()
        response = c.get(f"/posts/all")
        self.assertEqual(response.status_code, 200)

    def test_posts_filter_all_return_404_on_post_request(self):
        """*** Should I POST /posts/all, then return 404 ***"""
        c = Client()
        response = c.post(f"/posts/all")
        self.assertEqual(response.status_code, 404)

    def test_posts_filter_following_logged_in_return_200(self):
        """*** Should I GET /posts/following when logged in, return 200 ***"""
        u = createUser("foo", "foo@example.com", "example")
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/posts/following")
        self.assertEqual(response.status_code, 200)

    def test_posts_filter_all_return_all_posts(self):
        """*** Should I GET /posts/all, then return all posts ***"""
        u = createUser("foo", "foo@example.com", "example")
        m = "New post message 1"
        p = Post()
        p.post(m, u)
        m = "New post message 2"
        p = Post()
        p.post(m, u)
        c = Client()
        response = c.get(f"/posts/all")
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_posts_filter_following_return_404_on_logged_out_request(self):
        """*** Should I GET /posts/following when logged out, then return 404 ***"""
        c = Client()
        response = c.get(f"/posts/following")
        self.assertEqual(response.status_code, 404)

    def test_posts_filter_following_return_404_on_unrecognized_filter(self):
        """*** Should I GET /posts/unrecognized, then return 404 ***"""
        c = Client()
        response = c.get(f"/posts/unrecognized")
        self.assertEqual(response.status_code, 404)

    def test_posts_filter_following(self):
        """*** Should foo follow juan, then /posts/following should return juan's posts in reverse order ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        foo.follow(juan)
        m1 = "New post message 1"
        p = Post()
        p.post(m1, juan)
        m2 = "New post message 2"
        p = Post()
        p.post(m2, juan)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/posts/following")
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["message"], m2)
        self.assertEqual(data[1]["message"], m1)

    def test_posts_filter_following(self):
        """*** Should foo follow juan but not zoe, then /posts/following should return only juan's posts in reverse order ***"""
        foo = createUser("foo", "foo@example.com", "example")
        juan  = createUser("juan", "juan@example.com", "example")
        zoe = createUser("zoe", "zoe@example.com", "example")
        foo.follow(juan)
        m1 = "New post message 1"
        p = Post()
        p.post(m1, juan)
        m2 = "New post message 2"
        p = Post()
        p.post(m2, juan)
        m3 = "New post message 3"
        p = Post()
        p.post(m3, zoe)
        c = Client()
        c.login(username='foo', password='example')
        response = c.get(f"/posts/following")
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["message"], m2)
        self.assertEqual(data[1]["message"], m1)
        self.assertEqual(data[0]["user"]["username"], "juan")
        self.assertEqual(data[1]["user"]["username"], "juan")

if __name__ == "__main__":
    unittest.main()
