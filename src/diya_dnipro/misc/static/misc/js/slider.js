$(function () {
    var nextPos = 1;
    var timeout = 5000;
    var sliderTimer;

    var rotateActive = function() {
        var $active = $('.main_slider .pick.active');
        if ($active.next() && $active.next().length) {
            nextPos = $active.next().attr('data-pos');
        }
        else {
            nextPos = 1;
        }
        setActive(nextPos);
    };

    var setActive = function (pos) {
        $('.main_slider .active').removeClass('active');
        $('.main_slider .pick[data-pos="' + pos + '"]').addClass('active');
        $('.main_slider .wrapper[data-pos="' + pos + '"]').addClass('active');
        clearInterval(sliderTimer);
        sliderTimer = setInterval(rotateActive, timeout);
    };

    $('.main_slider .pick').on('click', function () {
        var $this = $(this);
        setActive($this.attr('data-pos'));
    });

    setActive(1);
});
