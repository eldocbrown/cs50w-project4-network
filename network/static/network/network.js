document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';

  // All posts event
  document.querySelector('#posts-link').addEventListener('click', (e) => {
    posts();
  });

  // All posts event
  const allPostsLink = document.querySelector('#allPosts')
  if (allPostsLink) {
    allPostsLink.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelector('#allPostsLabel').classList.add('active');
      document.querySelector('#followingPostsLabel').classList.remove('active');
      posts();
    });
  }

  // Following posts event
  const followingLink = document.querySelector('#followingPosts');
  if (followingLink) {
    followingLink.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelector('#allPostsLabel').classList.remove('active');
      document.querySelector('#followingPostsLabel').classList.add('active');
      following();
    });
  }

  // New post event
  const newPostLink = document.querySelector('#new-post-link');
  if (newPostLink) {
    newPostLink.addEventListener('click', (e) => {
      e.preventDefault();
      new_post();
    });
  }

  posts();

});

function new_post() {
  const postsView = document.querySelector('#posts-view');
  clearNode(postsView);
  postsView.style.display = 'none';
  document.querySelector('#posts-selector').style.display = 'none';
  document.querySelector('#new-post-view').style.display = 'block';
}

function posts() {

  recreatePostsView();
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';

  // Get latests mails from mailbox and render them
  fetch(`/posts/all`)
  .then(response => response.json())
  .then(data => {
      data.forEach(addPost);
  });
}

function following() {

  recreatePostsView();
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';

  // Get latests mails from mailbox and render them
  fetch(`/posts/following`)
  .then(response => response.json())
  .then(data => {
      data.forEach(addPost);
  });
}

async function addPost(contents) {
  // create post container
  const post = document.createElement('div');
  post.className = 'container p-3 my-3 border';
  post.setAttribute('id', contents.id);
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
  const heartSrc = '/static/network/image/heart.png';
  const heartSrcOutline = '/static/network/image/heart_outline.png';
  // If user is NOT authenticated
  if (!document.querySelector('#userNavItem')) {
    imageHeart.src = heartSrcOutline;
  // If user IS authenticated
  } else {
    // lookup if user is likes this post
    fetch(`/like/${contents.id}`)
    .then(response => response.json())
    .then(result => {
      if (result.message === 'true') {
        imageHeart.src = heartSrc;
        imageHeart.dataset.liking = true;
      } else {
        imageHeart.src = heartSrcOutline;
        imageHeart.dataset.liking = false;
      }

    // set pointer behaviour
    imageHeart.addEventListener('mouseover', () => {
      imageHeart.style.cursor = 'pointer';
    });
    imageHeart.addEventListener('mouseout', () => {
      imageHeart.style.cursor = 'auto';
    });
    imageHeart.addEventListener('click', (event) => {
      handleLikeClick(event);
    });
  });
  }



  post.append(imageHeart);
  const likeCount = document.createElement('small');
  likeCount.innerHTML = contents.likes;
  post.append(document.createTextNode("\u00A0"));
  post.append(likeCount);

  // add post to posts_view
  document.querySelector('#posts-view').append(post);
}

function clearNode(node) {
  node.innerHTML = '';
}

function recreatePostsView() {
  const postsView = document.querySelector('#posts-view');
  clearNode(postsView);
  const headingNode = document.createElement('h3');
  headingNode.innerHTML = 'Latest Posts';
  postsView.append(headingNode);
}

function handleLikeClick(event) {
  const heart = event.currentTarget;
  // if user likes this post
  if (heart.dataset.liking === 'true') {
    // TODO: unlike post
    console.log('true');
  //if user doesn't like this post
  } else {
    // TODO: like post
    console.log('false');
  }
}
