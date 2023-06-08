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

          fetch('/api/check-authentication/', { headers })
            .then(response => response.json())
            .then(data => {
              if (data.is_authenticated) {
                // Пользователь аутентифицирован
                this.postData('/api/orders/', Object.values(this.basket), { headers })
                  .then(data => {
                    alert('Запрос успешно выполнен');
                    this.order.id = data.id;
                    this.order.products = data.products;
                    this.basket = {};
                    location.assign('/order');
                  })
                  .catch(() => {
                    console.warn('Ошибка при создании заказа');
                  });
              } else {
                // Пользователь не аутентифицирован
                alert('Пользователь не аутентифицирован');
                location.assign('/login');
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