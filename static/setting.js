$(document).ready(() => {
  const $setting = $(".setting");

  $setting.click(item => {
    $setting.removeClass("is-active");
    $(item.target).addClass("is-active");
  });
});
