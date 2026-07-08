from django.db import models

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('manager', 'مدیرعامل و کارشناس رسمی مسکن'),
        ('investment', 'مشاور سرمایه‌گذاری ملکی'),
        ('rent', 'مشاور برتر اجاره'),
        ('sale', 'مشاور برتر فروش'),
        ('legal', 'متخصص حقوقی و اتاق مذاکره'),
    )
    
    name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='سمت')
    bio = models.TextField(verbose_name='بیوگرافی تخصصی')
    image = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name='عکس')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال باشد؟')

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"

    class Meta:
        verbose_name = 'عضو تیم'
        verbose_name_plural = 'اعضای تیم'
        ordering = ['order', 'name']
