const { createApp } = Vue;const { Mask, MaskInput, vMaska } = Maska;createApp({  delimiters: ['${', '}$'],  mixins: [window.mix ? window.mix : {}],  directives : {    maska : vMaska,  },  methods: {    postData(url, payload, config) {      return axios.post(url, payload, config ? config : {})        .then(response => {          return response.data ? response.data : (response.json ? response.json() : null);        })        .catch(() => {          console.warn('Метод ' + url + ' не реализован');          throw new Error('no "post" method');        });    },    getData(url, payload) {      return axios.get(url, { params: payload })        .then(response => {         //console.log('Получен ответ:', response);          return response.data ? response.data : (response.json ? response.json() : null);        })        .catch(error => {        //console.error('Ошибка при выполнении запроса:', error);          console.warn('Метод ' + url + ' не реализован');          throw new Error('no "get" method');        });    },    search() {    const filterSearch = this.filterSearch;      location.replace('/catalog/19');//      const filterSearch = this.filterSearch;//      this.getCatalogs(1, filterSearch);//    if (typeof page === 'undefined') {//        page = 1;//      };//    const PAGE_LIMIT = 6;////    this.getData('/api/catalog/', {//        page,//        filterSearch: this.filterSearch ? this.filterSearch : null,//        limit: PAGE_LIMIT,//      })//        .then((data) => {//          this.catalogCards = data.items;//          this.currentPage = data.currentPage;//          this.lastPage = data.lastPage;//          location.replace('/catalog/');//        })//        .catch(() => {//          console.warn('Ошибка при получении каталога');//        });    },    getCategories() {      this.getData('/api/categories/')        .then(data => {          this.categories = data;        })        .catch(() => {          console.warn('Ошибка получения категорий');          this.categories = [];        });    },    getBasket() {      const basket = {};      this.getData('/api/basket/')        .then(data => {          data.forEach(item => {            basket[item.id] = {              ...item            };          });          this.basket = basket;        })        .catch(() => {          console.warn('Ошибка при получении корзины');          this.basket = {};        });    },//    getLastOrder() {//      this.getData('/api/orders/active/')//        .then(data => {//        //console.log('Получены данные активного заказа:', data);//          this.order = {//            ...this.order,//            ...data//          };//        })//        .catch(error => {//        //console.error('Ошибка при получении активного заказа:', error);//          console.warn('Ошибка при получении активного заказа');//          this.order = {//            ...this.order//          };//        })//        .finally(() => {//         //console.log('Завершена функция getLastOrder. Значение this.order:', this.order);//          //alert(this.order);//        });//    },    addToBasket(item, count) {          const id = item.id;          const csrfToken = this.getCookie('csrftoken');          this.postData('/api/basket/', {            id: item.id,            count: count || 1          }, {            headers: {              'X-CSRFToken': csrfToken            }          })            .then(data => {              if (this.basket[id] && item.count >= this.basket[id].count) {                this.basket[id].count += count;                this.basket[id].price = data.price * this.basket[id].count;              } else {                this.basket[id] = data;              }              this.getBasket();            })            .catch(() => {              console.warn('Ошибка при добавлении заказа в корзину');            });        },        removeFromBasket(item, count) {            const id = item.id;            const csrfToken = this.getCookie('csrftoken');            let requestData = { id: id, count: count };            axios.delete('/api/basket/', {                data: requestData,                headers: {                    'X-CSRFToken': csrfToken                }            })                .then(response => {                    if (item.count > 1) {                        // Если count определено, значит нужно уменьшить количество продукта                        this.basket[id].count -= count;                        this.basket[id].price = response.data.price * this.basket[id].count;                    } else {                        // Если количество продукта равно 1, значит нужно полностью удалить продукт                            delete this.basket[id];                    }                    this.getBasket();                     if (this.basketCount.count === 0) {                            window.location.href = '/';                            };                })                .catch(() => {                    console.warn('Ошибка при удалении продукта из корзины');                });        },      getCookie(name) {      // Получение значения куки по имени      let cookieValue = null;      if (document.cookie && document.cookie !== '') {        const cookies = document.cookie.split(';');        for (let i = 0; i < cookies.length; i++) {          const cookie = cookies[i].trim();          // Does this cookie string begin with the name we want?          if (cookie.substring(0, name.length + 1) === name + '=') {            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));            break;          }        }      }      return cookieValue;    },  },  mounted() {    this.getCategories();    this.getBasket();    //this.getLastOrder();  },  computed: {    basketCount() {      return (        this.basket &&        Object.values(this.basket)?.reduce((acc, val) => {          acc.count += val.count;          acc.price += val.price * val.count;          return acc;        }, { count: 0, price: 0 })      ) ?? { count: 0, price: 0 };    }  },  data() {    return {      // catalog page      filters: {        price: {          minValue: 1,          maxValue: 500000,          currentFromValue: 1,          currentToValue: 300000        }      },      sortRules: [        { id: 'rating', title: 'Популярности' },        { id: 'price', title: 'Цене' },        { id: 'reviews', title: 'Отзывам' },        { id: 'date', title: 'Новизне' }      ],      topTags: [],      // reused data      categories: [],      categoriesFromServer: [],      // reused data      catalogFromServer: [],      orders: [],      cart: [],      paymentData: {},      basket: {},      order: {        orderId: null,        createdAt: '',        products: [],        fullName: '',        phone: '',        email: '',        deliveryType: '',        city: '',        address: '',        paymentType: '',        totalCost: 0,        status: ''      },       filterSearch: ''    };  },}).mount('#site');