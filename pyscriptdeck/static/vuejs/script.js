const appScript = new Vue({
  delimiters: ['[[',']]'],
  el: '#app-script',
  data: {
    error: null,
    loading: true,
    script: null,
    formData: {},
    running: false,
    runResult: null
  },
  methods: {
    run: function (submitEvent) {
      this.running = true;
      axios.post(url_api_get_scripts + '/' + this.script.id + '/_run', this.formData)
        .then(response => {
          this.runResult = response.data;
          this.running = false;
          this.error = null;
          this.refreshExecutionHistory();
        }).catch(error => {
          errorMessage = error;
          if (error.response.data && error.response.data.description) {
            errorMessage = `${error.response.data.name} - ${error.response.data.description}`
          }
          this.runResult = null;
          this.running = false;
          this.error = errorMessage;
        });
    },
    refreshExecutionHistory: function() {
      axios.get(url_api_get_scripts + '/' + this.script.id + '/executions')
        .then(response => {
          this.script.executions = response.data;
        });
    },
    onValueChange: function(paramId, paramNewValue) {
      this.formData[paramId] = paramNewValue;
    },
    resetForm: function() {
      this.script.params.forEach((param) => {
        const refParamScript = this.$refs['param-script-' + param.id];
        if (refParamScript && refParamScript.length > 0) {
          refParamScript[0].resetParamValue();
        }
      });
    }
  },
  mounted () {
    axios.get(url_api_get_scripts + '/' + script_id).then(response => {
      this.script = response.data;
      this.loading = false;
    });
  }
});
