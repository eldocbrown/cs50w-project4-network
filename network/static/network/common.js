const heartSrc = '/static/network/image/heart.png';
const heartSrcOutline = '/static/network/image/heart_outline.png';
const postLimit = 10;
var currentPage = 1;
var currentFilter = 'all';

function addPost(contents, containerId) {
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

    //if it is not my posts
    if (contents.user.username !== username) {
      // set pointer behaviour
      imageHeart.addEventListener('mouseover', () => {
        imageHeart.style.cursor = 'pointer';
      });
      imageHeart.addEventListener('mouseout', () => {
        imageHeart.style.cursor = 'auto';
      });
      imageHeart.addEventListener('click', (event) => {
        handleLikeClick(event, contents.id);
      });
    }
  });
  }

  post.append(imageHeart);
  const likeCount = document.createElement('small');
  likeCount.innerHTML = contents.likes;
  likeCount.id = 'likeCount'+ contents.id;
  post.append(document.createTextNode("\u00A0"));
  post.append(likeCount);

  // add post to posts_view
  document.querySelector(`#${containerId}`).append(post);
}

function clearNode(node) {
  node.innerHTML = '';
}

function evaluatePaginator(postCount) {
  // Previous link
  // First Page
  if (currentPage === 1) {
    document.querySelector('#previuosListItemPag').classList.add('disabled');
    document.querySelector('#previousLinkPag').setAttribute('tabIndex', '-1');
    document.querySelector('#previousLinkPag').setAttribute('aria-disabled', 'true');
  }
  // Other page
  else {
    document.querySelector('#previuosListItemPag').classList.remove('disabled');
    document.querySelector('#previousLinkPag').removeAttribute('tabIndex');
    document.querySelector('#previousLinkPag').removeAttribute('aria-disabled');
  }

  // Next link
  // No posts
  if (postCount < postLimit) {
    document.querySelector('#nextListItemPag').classList.add('disabled');
    document.querySelector('#nextLinkPag').setAttribute('tabIndex', '-1');
    document.querySelector('#nextLinkPag').setAttribute('aria-disabled', 'true');
  }
  // There are posts
  else {
    document.querySelector('#nextListItemPag').classList.remove('disabled');
    document.querySelector('#nextLinkPag').removeAttribute('tabIndex');
    document.querySelector('#nextLinkPag').removeAttribute('aria-disabled');
  }
}

function countPosts(jsonDataObj) {
  return jsonDataObj.length;
}

function addPaginationEvents() {
  // Next page event
  document.querySelector('#nextLinkPag').addEventListener('click', (event) => {
    let nextPage = currentPage + 1;
    currentPage = nextPage;
    if (currentFilter === 'all') { posts(nextPage); }
    else if (currentFilter === 'following') { following(nextPage); }
    else if (currentFilter === 'profile') { loadProfilePosts(profileusername, 'user-posts-view', nextPage); }
  });

  // Previous page event
  document.querySelector('#previousLinkPag').addEventListener('click', (event) => {
    let previousPage = currentPage - 1;
    currentPage = previousPage;
    if (currentFilter === 'all') { posts(previousPage); }
    else if (currentFilter === 'following') { following(previousPage); }
    else if (currentFilter === 'profile') { loadProfilePosts(profileusername, 'user-posts-view', previousPage); }
  });
}

function handleLikeClick(event, id) {
  const heart = event.currentTarget;
  // if user likes this post
  if (heart.dataset.liking === 'true') {
    fetch(`/unlike/${id}`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
    })
    .then(() => {
      const counter = document.querySelector(`#likeCount${id}`)
      counter.innerHTML = parseInt(counter.innerHTML) - 1
      heart.src = heartSrcOutline;
      heart.dataset.liking = 'false';
    });
  //if user doesn't like this post
  } else {
    fetch(`/like/${id}`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin'
    })
    .then(() => {
      const counter = document.querySelector(`#likeCount${id}`)
      counter.innerHTML = parseInt(counter.innerHTML) + 1
      heart.src = heartSrc;
      heart.dataset.liking = 'true'
    });
  }
}
