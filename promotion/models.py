from django.db import models


class Promotion(models.Model):
    category = models.ForeignKey('items.Category', on_delete=models.CASCADE,null=True,blank=True)
    order_num = models.IntegerField('Порядок вывода', default=100)
    name = models.CharField('Название акции', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='promotions/', blank=True)
    text = models.TextField('Текст', blank=True)
    is_active = models.BooleanField('Отображать?', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = "Акция"
        verbose_name_plural = "Акции"