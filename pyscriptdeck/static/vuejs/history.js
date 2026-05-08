const { createApp, ref, onMounted } = Vue;

const app = createApp({
  compilerOptions: {
    delimiters: ['[[',']]'],
  },
  setup() {
    const loading = ref(true);
    const executions = ref([]);

    onMounted(() => {
      axios.get(url_api_get_executions).then(response => {
        executions.value = response.data;
        loading.value = false;
      });
    });

    return {loading, executions};
  },
});
