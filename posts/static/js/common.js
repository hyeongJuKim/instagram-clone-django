/**
 * nav scroll fade
 */
function scrollFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        $('.nav').css('padding', '10px 0');
        $('.scrolldown-hide').fadeOut(200);
    } else {
        $('.nav').css('padding', '20px 0');
        $('.scrolldown-hide').fadeIn(200);
    }
}