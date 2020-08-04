const appIndex = new Vue({
  delimiters: ['[[',']]'],
  el: '#app-index',
  data: {
    loading: true,
    searchForm: {
      txt: '',
      group: null
    },
    scripts: [],
    filteredScripts: [],
    groups: []
  },
  methods: {
    filterScripts: function() {
      this.filteredScripts = this.scripts.filter(script => {
        if (this.searchForm.group && this.searchForm.group !== script.group) {
          return false;
        }
        if (this.searchForm.txt) {
          const splitTxtArray = this.searchForm.txt.toLowerCase().split(' ');
          return splitTxtArray.every(splitTxt =>
            script.id.toLowerCase().includes(splitTxt) ||
            script.name.toLowerCase().includes(splitTxt) ||
            script.description.toLowerCase().includes(splitTxt)
          )
        }
        return true;
      });
    }
  },
  watch: {
    searchForm: {
      handler: function(newValue, oldValue) {
        this.filterScripts();
      },
      deep: true
    }
  },
  mounted () {
    axios.get(url_api_get_scripts).then(response => {
      this.scripts = response.data;
      this.filteredScripts = this.scripts;
      this.loading = false;
    });

    axios.get(url_api_get_groups).then(response => {
      this.groups = response.data;
    });
  }
});
