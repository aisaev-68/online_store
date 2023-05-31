var mix = {
  methods: {
    getSettings() {
      this.getData("/api/settings/").then(data => {
        this.page_size = data.page_size;
      });
    },
  },

  mounted() {
    this.getSettings();
  },
  data() {
    return {
      page_size: ""
    };
  },
  //
};