function setCountdownInfo(){

    var archhacks_time = new Date(2016, 10, 4, 18);
    var now = new Date();

    var delta = Math.abs(archhacks_time - now) / 1000;

    var days = Math.floor(delta / 86400);
    delta -= days * 86400;
    $('#countdown-days-val').text(days);

    var hours = Math.floor(delta / 3600) % 24;
    delta -= hours * 3600;
    $('#countdown-hours-val').text(hours);

    var minutes = Math.floor(delta / 60) % 60;
    delta -= minutes * 60;
    $('#countdown-minutes-val').text(minutes);

    var seconds = delta % 60;
    $('#countdown-seconds-val').text(parseInt(seconds, 10));
}