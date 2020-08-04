const appHistory = new Vue({
  delimiters: ['[[',']]'],
  el: '#app-history',
  data: {
    loading: true,
    executions: null,
  },
  mounted () {
    axios.get(url_api_get_executions).then(response => {
      this.executions = response.data;
      this.loading = false;
    });
  }
});
