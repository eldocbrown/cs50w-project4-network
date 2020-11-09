document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';

  // All posts event
  document.querySelector('#all-posts-link').addEventListener('click', () => {
    posts();
  });

  // New post event
  document.querySelector('#new-post-link').addEventListener('click', (e) => {
    new_post(e);
  });

  // All posts event
  document.querySelector('#following-link').addEventListener('click', (e) => {
    following(e);
  });

  posts();

});

function posts() {
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';
  document.querySelector('#indexHeading').innerHTML = "Latest Posts";

  // Get latests mails from mailbox and render them
  fetch(`/posts/all`)
  .then(response => response.json())
  .then(data => {
      data.forEach(addPost);
  });
}

function new_post(event) {
  document.querySelector('#posts-view').style.display = 'none';
  document.querySelector('#new-post-view').style.display = 'block';
}

function following(event) {
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';
  document.querySelector('#indexHeading').innerHTML = "Latest Following Posts";
}

function addPost(contents) {
  // create post container
  const post = document.createElement('div');
  post.className = 'container p-3 my-3 border';
  // create user link
  const link = document.createElement('a');
  link.className = 'usernameLinkPost';
  link.href = '/profile/' + contents.user.username;
  post.append(link);
  // create user text
  const userText = document.createElement('strong');
  userText.innerHTML = contents.user.username;
  link.append(userText);
  // line break
  post.append(document.createElement('br'));
  // create message
  const message = document.createElement('small');
  message.innerHTML = contents.message;
  post.append(message);
  // line break
  post.append(document.createElement('br'));
  // create timestamped
  const timestampSmall = document.createElement('small');
  const timestampItalic = document.createElement('i');
  timestampItalic.innerHTML = contents.created_at;
  timestampSmall.append(timestampItalic);
  post.append(timestampSmall);
  // line break
  post.append(document.createElement('br'));
  // create like bar
  const imageHeart = document.createElement('img');
  imageHeart.id = 'postLikesheart';
  imageHeart.src = '/static/network/image/heart.png';
  post.append(imageHeart);
  // TODO: count likes
  const likeCount = document.createElement('small');
  likeCount.innerHTML = '0';
  post.append(document.createTextNode("\u00A0"));
  post.append(likeCount);

  // add post to posts_view
  document.querySelector('#posts-view').append(post);
}
