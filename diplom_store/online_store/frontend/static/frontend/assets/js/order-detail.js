var mix = {
  methods: {
    getOrderDetail() {

      this.id = location.pathname.startsWith('/order-detail/')
        ? Number(location.pathname.replace('/order-detail/', ''))
        : null;

      this.getData('/api/orders/' + this.id + '/')
        .then(data => {
          this.orderId = data.orderId;
          this.createdAt = data.createdAt;
          this.fullName = data.fullName;
          this.phone = data.phone;
          this.email = data.email;
          this.deliveryType = data.deliveryType;
          this.city = data.city;
          this.address = data.address;
          this.paymentType = data.paymentType;
          this.status = data.status;
          this.totalCost = data.totalCost;
          this.products = data.products;
          if (typeof data.paymentError !== 'undefined') {
            this.paymentError = data.paymentError;
          }
        })
        .catch(error => {
          console.warn('Ошибка при получении активного заказа');
        })
        .finally(() => {
          // console.log('Завершена функция getOrder');
          // alert(this.city);
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
    this.getOrderDetail();
  },
  data() {
    return {
      orderId: null,
      createdAt: null,
      fullName: null,
      phone: null,
      email: null,
      deliveryType: null,
      city: null,
      address: null,
      paymentType: null,
      status: null,
      totalCost: null,
      products: [],
      paymentError: null,
      payment_methods_choices: {},
      shipping_methods_choices: {}
    };
  }
};