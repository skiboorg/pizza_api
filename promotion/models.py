from django.db import models
from user.services import sendPush

class Promotion(models.Model):
    city = models.ForeignKey('items.City',on_delete=models.CASCADE, null=True, blank=True,verbose_name='Город')
    category = models.ForeignKey('items.Category', on_delete=models.CASCADE,null=True,blank=True)
    order_num = models.IntegerField('Порядок вывода', default=100)
    name = models.CharField('Название акции', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='promotions/', blank=True)
    text = models.TextField('Текст', blank=True)
    is_active = models.BooleanField('Отображать?', default=False)
    is_need_notify = models.BooleanField('Сделать расслку пушей после сохранения акции?', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def save(self, *args, **kwargs):
        if self.is_need_notify:
            sendPush(mode='promo', title='Новая акция', text=self.name, url='/promo', city=self.city)
            self.is_need_notify = False
        super(Promotion, self).save(*args, **kwargs)