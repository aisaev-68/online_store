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
          const authenticated = this.getCookie('is_authenticated');
          alert(authenticated)
          const headers = {
            'X-CSRFToken': csrfToken
          };
          if (!this.authenticated) {
            alert('Пользователь не аутентифицирован');
            // Перенаправление на страницу входа для анонимного пользователя
            location.assign('/login');
            return;
          }
          this.postData('/api/orders/', Object.values(this.basket), { headers })
            .then(data => {
              alert('Запрос успешно выполнен');
              this.order.id = data.id;
              this.order.products = data.products;
              this.basket = {};
              this.isAuthenticated = true;
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
          // Начинается ли эта строка cookie с имени, которое нам нужно
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      };
      alert('aaaa');
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