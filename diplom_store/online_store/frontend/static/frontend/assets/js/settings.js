var mix = {
  methods: {
    getSettings() {
      const csrfToken = this.getCookie('csrftoken');
      this.getData("/api/settings/", {
        headers: { 'X-CSRFToken': csrfToken }
      })
        .then(data => {
          this.page_size = data.page_size;
          this.payment_methods = data.payment_methods;
          this.shipping_methods = data.shipping_methods;
          this.order_status = data.order_status;

          // Установка списков выбора для каждого поля
          this.payment_methods_choices = data.payment_methods_choices;
          this.shipping_methods_choices = data.shipping_methods_choices;
          this.order_status_choices = data.order_status_choices;
        })
        .catch(() => {
          console.warn('Ошибка при получении настроек');
        });
    },
    changeSettings() {
      this.clearErrors();
      const csrfToken = this.getCookie('csrftoken');
      const requestData = {
        page_size: this.page_size,
        payment_methods: this.payment_methods,
        shipping_methods: this.shipping_methods,
        order_status: this.order_status,
      };

      this.postData("/api/settings/", requestData, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      })
        .then(() => {
          console.log('Настройки успешно изменены');
          this.settingUpdated = true;
          this.getSettings();
          this.clearErrors();
          // Дополнительные действия после успешного изменения настроек
        })
        .catch(() => {
          console.error('Ошибка при изменении настроек');
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
    },
    clearErrors() {
      // Очистка ошибок
      const errorFields = document.querySelectorAll('.error');
      errorFields.forEach(field => {
        field.classList.remove('error');
      });

      const errorTextElements = document.querySelectorAll('.error-text');
      errorTextElements.forEach(element => {
        element.remove();
      });
    },
  },
  mounted() {
    this.getSettings();
    //this.changeSettings();
  },
  data() {
    return {
      page_size: "",
      payment_methods: "",
      shipping_methods: "",
      order_status: "",
      settingUpdated: false,
      payment_methods_choices: {},
      shipping_methods_choices: {},
      order_status_choices: {},
    };
  }
};