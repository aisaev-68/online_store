var mix = {
    methods: {
        getSales() {
            this.getData("/api/sale/").then(data => {
                this.salesCards = data.salesCards;
                this.currentPage = data.currentPage;
                this.lastPage = data.lastPage;
            })
        },
    },
    mounted() {
        this.getSales();
    },
    data() {
        return {
            salesCards: [],
            currentPage: null,
            lastPage: 1
        }
    },
}