var mix = {
    methods: {
        getCartItems() {
            this.getData("/api/basket/")
              .then(data => {
                this.cartProducts = data.items
              });
        },
        submitBasket() {
          const csrfToken = this.getCookie('csrftoken');
          const headers = {
            'X-CSRFToken': csrfToken
          };

          this.postData('/api/orders/', Object.values(this.basket), { headers })
            .then(data => {
              this.order.id = data.id;
              this.order.products = data.products;
              this.basket = {};
              location.assign('/order');
            })
            .catch(() => {
              console.warn('Ошибка при создании заказа');
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
    },
    mounted() {
        this.getCartItems();
    },
    data() {
        return {
            cartProducts: [],
        }
    }
};