var mix = {
  methods: {
    getOrder() {
    alert("AAAAAAAAA");
     this.id = location.pathname.startsWith('/payment/')
        ? Number(location.pathname.replace('/payment/', '').replace('/',''))
        : null;

      this.getData('/api/orders/active/')
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

      const csrfToken = this.getCookie('csrftoken');
       if (this.month < 1 && this.month > 12) {

       };

      this.postData('/api/payment/', {
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
          //alert('Успешная оплата');
          this.number = '';
          this.name = '';
          this.year = '';
          this.month = '';
          this.code = '';
          location.assign('/progress-payment/');
        })
        .catch(() => {
          console.warn('Ошибка при оплате');
        });
    },
     generateRandomData: function() {
      var names = ['John', 'Jane', 'Alex', 'Emily', 'Michael', 'Emma', 'David', 'Olivia', 'Daniel', 'Sophia'];
      var surnames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson'];

      // Generate random bill number
      var billNumber = '';
      do {
        billNumber = Math.random() + '';
        billNumber = billNumber.slice(-9, -1);
      } while (parseFloat(billNumber) % 2 !== 0);
      billNumber = billNumber.slice(0, 4) + ' ' + billNumber.slice(4, 8);
      this.number = billNumber;

      // Generate random month
      var currentMonth = new Date().getMonth() + 1; // Get current month (1-12)
      var randomMonth = Math.floor(Math.random() * (12 - currentMonth + 1)) + currentMonth;
      this.month = randomMonth < 10 ? '0' + randomMonth : randomMonth;

      // Generate random year
      var currentYear = new Date().getFullYear(); // Get current year
      var randomYear = Math.floor(Math.random() * (2030 - currentYear + 1)) + currentYear;
      this.year = randomYear;

      // Generate random card code (CVV)
      var randomCode = Math.floor(Math.random() * 900) + 100;
      this.code = randomCode;

      // Generate random name
      var randomName = surnames[Math.floor(Math.random() * surnames.length)] + ' ' +
        names[Math.floor(Math.random() * names.length)];
      this.name = randomName;
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