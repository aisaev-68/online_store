var mix = {
  methods: {
    getOrder(orderId) {
    //alert(orderId);
      this.getData('/api/orders/active')
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

    getSettings() {
      const csrfToken = this.getCookie('csrftoken');
      this.getData('/api/settings/', {
        headers: { 'X-CSRFToken': csrfToken }
      })
        .then(data => {
          this.page_size = data.page_size;
          this.express = data.express;
          this.standard = data.standard;
          this.amount_free = data.amount_free;
          this.payment_methods = data.payment_methods;
          this.shipping_methods = data.shipping_methods;
          this.payment_methods_choices = data.payment_methods_choices;
          this.shipping_methods_choices = data.shipping_methods_choices;
        })
        .catch(() => {
          console.warn('Ошибка при получении настроек');
        });
    },
    confirmOrder() {
      const csrfToken = this.getCookie('csrftoken');
      const keys = Object.keys(this.payment_methods_choices);
      const paymentMethod = keys[1];
      if (this.orderId) {
        const formData = {
          orderId: this.orderId,
          createdAt: this.createdAt,
          fullName: this.fullName,
          phone: this.phone,
          email: this.email,
          deliveryType: this.deliveryType,
          city: this.city,
          address: this.address,
          paymentType: this.paymentType,
          totalCost: this.totalCost,
          status: this.status,
          products: this.products
        };
        this.postData('/api/orders/' + this.orderId + '/', formData, {
          headers: {
            'X-CSRFToken': csrfToken
          }
        })
          .then(() => {
            alert(this.fullName);

            if (this.paymentType === paymentMethod) {
              location.replace('/payment/' + this.orderId + '/');
            } else {
              location.replace('/payment-someone/');
            }
          })
          .catch(() => {
            console.warn('Ошибка при подтверждении заказа');
          });
      }
    },
    updateTotalCost() {
      const keys = Object.keys(this.shipping_methods_choices);
      const shippingMethod = keys[1];
      alert(shippingMethod);
      alert(this.totalCost);
      if (this.deliveryType === shippingMethod) {
        this.totalCost += this.express;
      } else {
        if (this.totalCost < this.amount_free) {
          this.totalCost += this.standard;
        } else {
          this.totalCost = this.totalCost;
        }
      }
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
    this.getOrder(this.orderId);
    this.getSettings();
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