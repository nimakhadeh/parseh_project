from django.db import models
from properties.models import Property

class ContactRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    property = models.ForeignKey(
        Property, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='ملک مرتبط'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ دریافت')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده؟')

    def __str__(self):
        return f"{self.name} - {self.phone[:4]}***"

    class Meta:
        verbose_name = 'درخواست تماس'
        verbose_name_plural = 'درخواست‌های تماس'
        ordering = ['-created_at']
