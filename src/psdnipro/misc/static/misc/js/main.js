$(function () {
    setInterval(function () {
        $('header nav ul li.nav-item' + ':not(:hover)').removeClass('hovered');
    }, 1000);
    $('header nav ul li.nav-item').hover(function () {
        var $this = $(this);
        $('header nav ul li.nav-item').removeClass('hovered');
        $this.addClass('hovered');
    });
});
