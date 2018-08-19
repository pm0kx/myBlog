$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });

  $(".nav").find("li").each(function () {
    var a = $(this).find("a:first")[0];
    if ($(a).attr("href") === location.pathname) {
        $(this).addClass("active");
    } else {
        $(this).removeClass("active");
    }
  });

});