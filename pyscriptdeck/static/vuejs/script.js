const { createApp, ref, reactive, computed, onMounted } = Vue;

const app = createApp({
  compilerOptions: {
    delimiters: ['[[', ']]']
  },
  setup() {
    const loading = ref(true);
    const error = ref(null);
    const script = ref(null);
    const formData = reactive({});
    const running = ref(false);
    const runResult = ref(null);

    function run(submitEvent) {
      running.value = true;
      axios.post(url_api_get_scripts + '/' + script.value.id + '/_run', formData)
        .then(response => {
          runResult.value = response.data;
          running.value = false;
          error.value = null;
          refreshExecutionHistory();

        }).catch(error => {
          errorMessage = error;
          if (error.response.data && error.response.data.description) {
            errorMessage = `${error.response.data.name} - ${error.response.data.description}`
          }
          runResult.value = null;
          running.value = false;
          error.value = errorMessage;
        });
    }

    function refreshExecutionHistory() {
      axios.get(url_api_get_scripts + '/' + script.value.id + '/executions')
        .then(response => {
          script.value = {...script.value, executions: response.data};
        });
    }

    function onValueChange(paramId, paramNewValue) {
      formData[paramId] = paramNewValue;
    }

    function resetFormData() {
      script.value?.params?.forEach((param) => {
          formData[param.id] = param.default;
      });
    }

    onMounted(() => {
      axios.get(url_api_get_scripts + '/' + script_id).then(response => {
        script.value = response.data;
        resetFormData();
        loading.value = false;
      });
    })

    return {
      loading, error, script, formData, running, runResult,
      run, onValueChange, resetFormData, formatTime
    };
  }
});
