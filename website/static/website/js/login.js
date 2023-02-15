$(document).ready(function () {
//toggles active class between tabs by clicking on header links
    $('.header-item').on('click', function (e) {
        e.preventDefault();
        $(this).addClass('activated');
        $(this).siblings().removeClass('activated');


//changes login to register view and vice versa
        let target_href = $(this).attr('href');
        if (target_href === '#register' && $(target_href).css('display') === 'none') {
            $('.dish').addClass("activated");
            setTimeout(function () {
                $('.dish').css("background-image", " url('http://mycoreproject.ir/images/register-dish.png'");
            }, 300);

        } else if (target_href === '#login' && $(target_href).css('display') === 'none') {
            $('.dish').addClass("activated");
            setTimeout(function () {
                $('.dish').css("background-image", " url('http://mycoreproject.ir/images/login-dish.png'");
            }, 300);
        } else {

        }

        $('.form-holder > .form').not(target_href).hide();
        $(target_href).fadeIn(850);

        setTimeout(function () {
            $('.dish').removeClass('activated');
        }, 600);

    });
});