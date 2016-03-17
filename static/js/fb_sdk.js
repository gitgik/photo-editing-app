window.fbAsyncInit = function() {
    FB.init({
        appId      : '1675743882699372',
        status     : true,
        xfbml      : true,
        version    : 'v2.5'
    });
};

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "//connect.facebook.net/en_US/all.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
