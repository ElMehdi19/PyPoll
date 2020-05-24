let domCookies = document.cookie;
let cookiesObj = {};
domCookies = domCookies.split(';').map(cookie => {
    return cookie.split('=');
});
domCookies.forEach(cookie => {
    cookiesObj[cookie[0]] = cookie[1];
});