Vue.filter('formatTime', function(value) {
    if (value) {
        return moment.unix(value).format('HH:mm:ss')
    }
});

Vue.filter('formatDatetime', function(value) {
    if (value) {
        return moment.unix(value).format('DD/MM/YYYY - HH:mm:ss')
    }
});
