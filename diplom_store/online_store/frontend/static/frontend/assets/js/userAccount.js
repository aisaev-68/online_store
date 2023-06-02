var mix = {
  methods: {
    getUserAccount() {
      this.getData("/api/account/").then(data => {
        this.firstname = data.first_name;
        this.lastname = data.last_name;
        this.surname = data.surname;
        this.avatar = data.avatar;
        this.orders = data.orders;
      });
    },
  },

  mounted() {
    this.getUserAccount();
  },
  data() {
    return {
      lastname: "",
      firstname: "",
      surname: "",
      avatar: {},
      orders: [],
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
