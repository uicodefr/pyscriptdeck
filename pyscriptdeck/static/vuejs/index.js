const { createApp, ref, reactive, computed, onMounted } = Vue;

const app = createApp({
  compilerOptions: {
    delimiters: ['[[',']]'],
  },
  setup() {
    const loading = ref(true);
    const scripts = ref([]);
    const groups = ref([]);
    const searchForm = reactive({
      txt: '',
      group: null
    });

    const filteredScripts = computed(() => {
      return scripts.value.filter(script => {
        if (searchForm.group && searchForm.group !== script.group) {
          return false;
        }
        if (searchForm.txt) {
          const splitTxtArray = searchForm.txt.toLowerCase().split(' ');
          return splitTxtArray.every(splitTxt =>
            script.id.toLowerCase().includes(splitTxt) ||
            script.name.toLowerCase().includes(splitTxt) ||
            script.description.toLowerCase().includes(splitTxt)
          );
        }
        return true;
      });
    });

    onMounted(() => {
      axios.get(url_api_get_scripts).then(response => {
        scripts.value = response.data;
        loading.value = false;
      });

      const loadGroups = axios.get(url_api_get_groups).then(response => {
        groups.value = response.data;
      });
    });

    return {loading, groups, searchForm, filteredScripts};
  }
});
