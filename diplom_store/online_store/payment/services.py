import random
import queue
import threading

class PaymentService:
    def __init__(self):
        self.payment_queue = queue.Queue()

    def process_payment(self, card_number):
        # Создаем словарь с информацией о платеже
        payment_data = {
            'card_number': card_number,
            'status': None
        }
        # Добавляем информацию о платеже в очередь
        self.payment_queue.put(payment_data)
        return payment_data

    def payment_worker(self):

        while True:
            # Получаем информацию о платеже из очереди
            payment_data = self.payment_queue.get()
            card_number = payment_data['card_number']
            try:
                # Проверяем логику оплаты
                if card_number % 2 == 0 and card_number % 10 != 0:
                    # Платеж подтвержден, если номер четный и не заканчивается на ноль
                    payment_data['status'] = 'Paid'
                else:
                    # Устанавливаем статус ошибки и код ошибки в информацию о платеже
                    payment_data['status'] = 'Payment error'
            except Exception as e:
                # Обрабатываем возможные исключения
                payment_data['status'] = 'Payment error'
            finally:
                # Отмечаем задачу платежа как выполненную
                self.payment_queue.task_done()

    def start_payment_processing(self, num_workers=1):
        # Запускаем указанное количество рабочих потоков для обработки платежей
        for _ in range(num_workers):
            worker_thread = threading.Thread(target=self.payment_worker)
            worker_thread.daemon = True
            worker_thread.start()
