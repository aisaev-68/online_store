var mix = {
  methods: {
    checkPaymentStatus() {
      const orderId = location.pathname.startsWith('/progress-payment/')
        ? Number(location.pathname.replace('/progress-payment/', '').replace('/', ''))
        : null;
       // alert("PROGRESS")
      //alert(orderId);

      this.getData('/api/payment/' + orderId + '/')
        .then(data => {
          this.status = data.status;
          //alert("STATUS");
         // alert(this.status);
         setTimeout(() => {
               location.replace('/account/');
            }, 15000); // Переход через 30 секунд
//          if (this.status === 'Paid') {
//            location.replace('/account/');
//          } else if (this.status === 'Payment error') {
//            location.replace('/account/');
//          } else {
//            setTimeout(this.checkPaymentStatus, 100);
//          }
        })
        .catch((error) => {
          console.warn('Ошибка при проверке статуса оплаты', error);
          //this.$router.push('/payment-error');
        });
    }
  },
  mounted() {
    this.checkPaymentStatus();
  }
};
