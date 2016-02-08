$(window).scroll(
    function(){
        var $window = $(window);
        var $body = $("body");
        if($body.height()-($window.height()+$window.scrollTop()) <= 100) {
           $body.height($body.height() + 500);
        }
        if($body.width()-($window.width()+$window.scrollLeft()) <= 100) {
           $body.width($body.width() + 500);
        }
})
