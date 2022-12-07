from django.db import models

class Seller(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)

class Table(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)


StatusEnum = (
    ("PENDING", "pending"),
    ("DELIVERED", "delivered")
)

PaymentTypeEnum = (
    ("CARD", "card"),
    ("CASH", "cash")
)

StatusPaymentEnum = (
    ("PENDING", "pending"),
    ("PAID", "paid")
)


class Payment(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    totalPayment = models.DecimalField(max_digits=10, decimal_places=2)
    paymentType = models.CharField(max_length=255, choices=PaymentTypeEnum)
    statusPayment = models.CharField(max_length=255, choices=StatusPaymentEnum)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.table)
        

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('inv.Product', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusEnum)
    created_at = models.DateTimeField(auto_now_add=True)
    close = models.BooleanField(default=False)

    def __str__(self):
        return str(self.table)

