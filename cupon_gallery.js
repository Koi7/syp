$(function () {
    var count_cupon = $('.wrapper_list li').length,
        w_cupon = parseInt($('.wrapper_list li').width() + 10),
        direction = true,
        speed = 0.05;

    var width_gallery_cupon = count_cupon * w_cupon;
    var margin_left = -1 * ((5 * (w_cupon)) - width_gallery_cupon);

    $('.wrapper_list ul').width(width_gallery_cupon);

    function moveLeft(way) {
        direction = true;
        $('.wrapper_list ul').stop().animate({
            marginLeft: -margin_left
        }, way / speed, 'linear', function () {
            moveRight(margin_left);
        });
    }

    function moveRight(way) {
        direction = false;
        $('.wrapper_list ul').stop().animate({
            marginLeft: 0
        }, way / speed, 'linear', function () {
            moveLeft(margin_left);
        });
    }

    moveLeft(margin_left);

    $('.wrapper_list ul').hover(function () {
        $(this).stop();
    }, function () {
        var left = parseInt($(this).css('margin-left'));
        if (direction)
            moveLeft(margin_left + left);
        else
            moveRight(-1 * left);
    });

    $('.left_arrow').click(function(e) {
        e.preventDefault();
        var ml = parseInt($('.wrapper_list ul').css('margin-left')),
            left;
        if (-ml < w_cupon)
            left = 0;
        else
            left = ml + w_cupon;
        $('.wrapper_list ul').stop().animate({
            marginLeft: left
        }, 500, 'linear', function () {
            if (direction)
                moveLeft(margin_left - left);
            else
                moveRight(-left);
        });
    });

    $('.right_arrow').click(function (e) {
        e.preventDefault();
        var ml = parseInt($('.wrapper_list ul').css('margin-left')),
                right;
        if (-(ml - w_cupon) < margin_left) {
            right = ml - w_cupon;
        } else {
            right = -margin_left;
        }
        $('.wrapper_list ul').stop().animate({
            marginLeft: right
        }, 500, 'linear', function () {
            if (direction)
                moveLeft(margin_left + right);
            else
                moveRight(-right);
        });
    });

});