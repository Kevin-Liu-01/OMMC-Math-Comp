$(document).ready(() => {
  console.log("heya");

  $(":header").css("font-family", "Open Sans, sans-serif");
  $(":not(:header)").css("font-family", "Raleway, sans-serif");
  $(".title").css("font-family", "Open Sans, sans-serif");

  const $burger = $(".navbar-burger")
  if ($burger)
    $burger.click(() => {
      $(".navbar-menu").toggleClass("is-active");
      $burger.toggleClass("is-active");
    });

  // const $hasColor = $(".has-color");
  // if ($hasColor) {
  //   $hasColor.css({
  //     "background-color": "#AB3942",
  //     "color": "white",
  //   });
  //   $hasColor.find("*").css({
  //     "background-color": "#AB3942",
  //     "color": "white",
  //   });
  // }

  const $submit = $("#submit");
  if ($submit)
    $submit.click(() => {
      $submit.addClass("is-loading");

      setTimeout(() => {
        $submit.removeClass("is-loading");
      }, 3000);
    });

  const $password = $("#password");
  const $toggle = $("#toggle");

  if ($toggle)
    $toggle.click(() => {
      if ($toggle.hasClass("mdi-eye")) {
        $password.attr("type", "text");
        $toggle.removeClass("mdi-eye").addClass("mdi-eye-off");
      } else {
        $password.attr("type", "password");
        $toggle.removeClass("mdi-eye-off").addClass("mdi-eye");
      }
    });

  const $stats = $("#stats");
  if ($stats)
    $stats.css("padding", 15);
});
