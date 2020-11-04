document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#all-posts-view').style.display = 'none';
  document.querySelector('#new-post-view').style.display = 'none';
  document.querySelector('#following-view').style.display = 'none';

  // All posts event
  document.querySelector('#all-posts-link').addEventListener('click', (e) => {
    posts(e);
  });

  // New post event
  document.querySelector('#new-post-link').addEventListener('click', (e) => {
    new_post(e);
  });

  // All posts event
  document.querySelector('#following-link').addEventListener('click', (e) => {
    following(e);
  });

});

function posts(event) {
  document.querySelector('#all-posts-view').style.display = 'block';
  document.querySelector('#new-post-view').style.display = 'none';
  document.querySelector('#following-view').style.display = 'none';
}

function new_post(event) {
  document.querySelector('#all-posts-view').style.display = 'none';
  document.querySelector('#new-post-view').style.display = 'block';
  document.querySelector('#following-view').style.display = 'none';
}

function following(event) {
  document.querySelector('#all-posts-view').style.display = 'none';
  document.querySelector('#new-post-view').style.display = 'none';
  document.querySelector('#following-view').style.display = 'block';
}
