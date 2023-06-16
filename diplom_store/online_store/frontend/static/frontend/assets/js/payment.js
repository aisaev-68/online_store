var mix = {
  methods: {
    getOrder() {
    alert(location.pathname.replace('/payment/', '').replace('/', ''))
      this.id = location.pathname.startsWith('/payment/')
        ? Number(location.pathname.replace('/payment/', '').replace('/', ''))
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


    submitPayment() {
      const orderId = location.pathname.startsWith('/payment/')
        ? Number(location.pathname.replace('/payment/', '').replace('/', ''))
        : null;
      const csrfToken = this.getCookie('csrftoken');
       if (this.month < 1 && this.month > 12) {

       };

      this.postData(`/api/payment/${orderId}/`, {
        name: this.name,
        number: this.number,
        year: this.year,
        month: this.month,
        code: this.code
      }, {
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(() => {
          alert('Успешная оплата');
          this.number = '';
          this.name = '';
          this.year = '';
          this.month = '';
          this.code = '';
          location.assign('/');
        })
        .catch(() => {
          console.warn('Ошибка при оплате');
        });
    },
    getCookie(name) {
      // Получение значения куки по имени
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
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
        this.getOrder();
   },
  data() {
    return {
      number: '',
      month: '',
      year: '',
      name: '',
      code: ''
    };
  }
};