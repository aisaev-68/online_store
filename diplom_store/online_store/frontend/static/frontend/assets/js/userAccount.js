var mix = {
  methods: {
    getUserAccount() {
      const csrfToken = this.getCookie('csrftoken');
      this.getData("/api/account/", {
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(data => {
          this.firstname = data.first_name;
          this.lastname = data.last_name;
          this.surname = data.surname;
          this.avatar = data.avatar;
          this.order = data.order;
        });
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  },

  mounted() {
    this.getUserAccount();
  },
  data() {
    return {
      lastname: "",
      firstname: "",
      surname: "",
      avatar: "",
      order: "",
    };
  },
  computed: {
    fullName() {
      return [this.lastname, this.firstname, this.surname].join(" ");
    },
    displayContent() {
      return this.avatar ? this.avatar : this.fullName;
    },
  },
};
