from django.db import models
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    PRODUCTS_TYPE = (
        ('robot', '家用机器人'),
        ('monitoring', '智能监控'),
        ('face', '人脸识别解决方案'),
    )
    title = models.CharField(max_length=50, verbose_name='产品标题')
    description = models.TextField(verbose_name='产品详细描述')
    product_type = models.CharField(
        choices=PRODUCTS_TYPE, max_length=50, verbose_name='产品类型')
    price = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True, null=True, verbose_name='产品价格')
    publish_date = models.DateTimeField(
        max_length=20, default=timezone.now, verbose_name="发布时间")
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ('-publish_date',)


class ProductImg(models.Model):
    product = models.ForeignKey(Product,
                                related_name='product_imgs',
                                verbose_name='产品',
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Product/', blank=True, verbose_name='产品图片')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'
