var mix = {
  methods: {
    submitPayment() {
      const csrfToken = this.getCookie('csrftoken');

      this.postData('/api/payment/',
        {
          name: this.name,
          number: this.number,
          year: this.year,
          month: this.month,
          code: this.code
        },
        {
          headers: {
            'X-CSRFToken': csrfToken
          }
        }
      )
        .then(() => {
          alert('Успешная оплата');
          this.number = '';
          this.name = '';
          this.year = '';
          this.month = '';
          this.code = '';
          //location.assign('/');
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