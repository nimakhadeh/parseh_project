from django.db import models
from django.utils.text import slugify

class Property(models.Model):
    TRANSACTION_TYPES = (
        ('sale', 'فروش'),
        ('rent', 'اجاره'),
    )
    
    title = models.CharField(max_length=200, verbose_name='عنوان ملک')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='نامک')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت (تومان)')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES, verbose_name='نوع معامله')
    area = models.PositiveIntegerField(verbose_name='متراژ (متر مربع)')
    rooms = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد اتاق')
    address = models.TextField(default='فاطمی، خ جویبار، سر بن‌بست بهمن', verbose_name='آدرس')
    image = models.ImageField(upload_to='properties/', verbose_name='تصویر شاخص')
    is_published = models.BooleanField(default=True, verbose_name='منتشر شود؟')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = 'ملک‌ها'
        ordering = ['-created_at']