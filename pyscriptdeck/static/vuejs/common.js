function formatTime(value) {
  if (value) {
    return moment.unix(value).format('HH:mm:ss');
  }
};

function formatDatetime(value) {
  if (value) {
    return moment.unix(value).format('DD/MM/YYYY - HH:mm:ss');
  }
};
