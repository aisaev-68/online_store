var mix = {
    methods: {
        getHistoryOrder(page) {
        if (typeof page === 'undefined') {
            page = 1;
          }
            this.getData("/api/orders")
              .then(data => {
                this.orders = data
                this.currentPage = data.currentPage;
                this.lastPage = data.lastPage;
              }).catch(() => {
                this.orders = []
                console.warn('Ошибка при получении списка заказов')
            })
            //alert(this.orders)
        }
    },
    mounted() {
        this.getHistoryOrder();
    },
    data() {
        return {
            orders: [],
            currentPage: null,
            lastPage: 1,
        }
    }
}