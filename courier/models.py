from django.db import models

class Courier(models.Model):
    city = models.ForeignKey('items.City', on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField('ФИО', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон (формат номера 79991112233)', max_length=255, blank=True, null=True)
    notification_id = models.CharField(max_length=255, blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    have_orders_in_delivery = models.BooleanField(default=False)

class CourierOrder(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE,blank=True,null=True,related_name='orders')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE,blank=True,null=True)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.order.is_assing = True
        self.order.courier = self.courier
        self.order.save()
        super(CourierOrder, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

