function stretchAndShrink() {
  $('h1').animate({ letterSpacing: '16px' }, 800);
  $('h1').animate({ letterSpacing: '2px' }, 800);
}

$(document).ready(stretchAndShrink)
