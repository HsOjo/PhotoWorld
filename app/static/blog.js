// 页面动画，课外内容，有兴趣的读者可自行学习。
function load_posts() {
    let blog_posts = $('.blog-post');
    blog_posts.hide();
    blog_posts.each(function (i, v) {
        setTimeout(function () {
            $(v).fadeIn(300);
        }, i * 100);
    });
}
