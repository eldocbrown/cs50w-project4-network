document.addEventListener('DOMContentLoaded', function() {
  evaluateFollowStatus();
  const buttonFollow = document.querySelector('#buttonFollow');
  if (buttonFollow !== null) {
    buttonFollow.addEventListener('click', (event) => {
      handleFollowClick(event);
    });
  }
})

function evaluateFollowStatus() {
  // if buttonFollow exists
  const buttonFollow = document.querySelector('#buttonFollow');
  if (buttonFollow !== null) {
    // if i am following this users
    if (buttonFollow.dataset.following === 'True') {
      // show button text FOLLOWING (filled blue)
      buttonFollow.className = 'btn-sm btn-primary rounded-pill';
      buttonFollow.innerHTML = 'Following';
      // show button text UNFOLLOW on mouseover (filled red)
      buttonFollow.addEventListener('mouseover', (event) => {
        buttonFollow.className = 'btn-sm btn-danger rounded-pill';
        buttonFollow.innerHTML = 'Unfollow';
      });
      // show button text UNFOLLOW on mouseover (filled red)
      buttonFollow.addEventListener('mouseout', (event) => {
        buttonFollow.className = 'btn-sm btn-primary rounded-pill';
        buttonFollow.innerHTML = 'Following';
      });
    } else {
      // show button text FOLLOW (outlined blue)
      buttonFollow.className = 'btn-sm btn-outline-primary rounded-pill';
      buttonFollow.innerHTML = 'Follow';
    }
  }
}

function handleFollowClick(event) {
  if (event.currentTarget.dataset.following === 'True') {
    // TODO: put unfollow
    // TODO: .then event.currentTarget.dataset.following = False
  } else {
    // TODO: put follow
    // TODO: .then event.currentTarget.dataset.following = True
  }
  evaluateFollowStatus();
  event.currentTarget.blur();
}
