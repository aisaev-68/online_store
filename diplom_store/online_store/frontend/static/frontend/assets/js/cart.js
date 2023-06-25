var mix = {
    methods: {
        getCartItems() {
            this.getData("/api/basket/")
              .then(data => {
                this.cartProducts = data.items
              });
        },

        checkAuthentication() {
          const csrfToken = this.getCookie('csrftoken');
          const headers = {
            'X-CSRFToken': csrfToken
          };

          this.getData('/api/check-authentication/', { headers })
            .then(response => {
            this.is_authenticated = response.data.is_authenticated;
            })
            .catch(error => {
              console.warn('Ошибка при проверке аутентификации пользователя:', error);
            });
        },

        submitBasket(is_authenticated) {
            const csrfToken = this.getCookie('csrftoken');
            const headers = {
                'X-CSRFToken': csrfToken
            };
            this.getData('/api/check-authentication/', { headers })
                .then(response => {
                    if (response.is_authenticated && this.basketCount) {
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
                    } else {
                        location.replace('/login/');
                    }
                })
                .catch(() => {
                    console.warn('Ошибка при проверке аутентификации пользователя');
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
      return cookieValue;
    },
    },
    mounted() {
        this.getCartItems();
    },
    data() {
        return {
            cartProducts: [],
            is_authenticated: false
        }
    }
};