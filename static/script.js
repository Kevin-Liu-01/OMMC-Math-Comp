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

  const $submit = $("#submit");
  if ($submit)
    $submit.click(() => {
      $submit.addClass("is-loading");

      setTimeout(() => {
        $submit.removeClass("is-loading");
      }, 3000);
    });
});
