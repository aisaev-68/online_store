var mix = {
    methods: {
        getOrder(orderId) {
            this.getData('/api/orders/active').then(data => {
            console.log('Получены данные активного заказа:', data);
                this.orderId = data.orderId
                this.createdAt = data.createdAt
                this.fullName = data.fullName
                this.phone = data.phone
                this.email = data.email
                this.deliveryType = data.deliveryType
                this.city = data.city
                this.address = data.address
                this.paymentType = data.paymentType
                this.status = data.status
                this.totalCost = data.totalCost
                this.products = data.products
                if (typeof data.paymentError !== 'undefined'){
                    this.paymentError = data.paymentError
                }

            })
             .catch(error => {
              console.error('Ошибка при получении активного заказа:', error);
              console.warn('Ошибка при получении активного заказа');
            })
            .finally(() => {
              console.log('Завершена функция getOrder');

              alert(this.city);
            });
        },
        confirmOrder() {
            if (this.order) {
                this.postData('/api/orders/' + this.order, {
                   ...this.order
                })
                    .then(() => {
                        alert('Заказ подтвержден')
                        location.replace('/payment')
                    })
                    .catch(() => {
                        console.warn('Ошибка при подтверждения заказа')
                    })
            }
        }
    },
    mounted() {
        //this.getOrder(orderId);

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
        }
    },
}