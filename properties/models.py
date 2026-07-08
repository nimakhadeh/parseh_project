from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Property(models.Model):
    TRANSACTION_TYPES = (
        ('sale', 'فروش'),
        ('rent', 'اجاره'),
    )
    
    # اطلاعات پایه
    title = models.CharField(max_length=200, verbose_name='عنوان ملک')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='نامک')
    description = models.TextField(verbose_name='توضیحات')
    
    # اطلاعات مالی
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت (تومان)')
    deposit = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='ودیعه (تومان)')
    rent = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='اجاره ماهیانه (تومان)')
    
    # اطلاعات فنی
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES, verbose_name='نوع معامله')
    area = models.PositiveIntegerField(verbose_name='متراژ (متر مربع)')
    rooms = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد اتاق')
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='طبقه')
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='تعداد کل طبقات')
    year_built = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال ساخت')
    
    # امکانات
    has_elevator = models.BooleanField(default=False, verbose_name='آسانسور')
    has_parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    has_warehouse = models.BooleanField(default=False, verbose_name='انباری')
    has_balcony = models.BooleanField(default=False, verbose_name='بالکن')
    
    # موقعیت مکانی
    address = models.TextField(default='فاطمی، خ جویبار، سر بن‌بست بهمن', verbose_name='آدرس')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='عرض جغرافیایی')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='طول جغرافیایی')
    
    # ارتباط با مشاور
    advisor = models.ForeignKey(
        'team.TeamMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='مشاور ملک'
    )
    
    # تصاویر
    image = models.ImageField(upload_to='properties/', verbose_name='تصویر شاخص')
    image_2 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='تصویر ۲')
    image_3 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='تصویر ۳')
    image_4 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='تصویر ۴')
    
    # وضعیت
    is_published = models.BooleanField(default=True, verbose_name='منتشر شود؟')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه باشد؟')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    
    # زمان
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = 'ملک‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_type']),
            models.Index(fields=['price']),
            models.Index(fields=['is_published']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.get_transaction_type_display()}"

    def get_absolute_url(self):
        """دریافت لینک جزئیات ملک"""
        return reverse('property_detail', kwargs={'slug': self.slug})

    def get_price_display(self):
        """نمایش قیمت به صورت خوانا"""
        if self.transaction_type == 'sale':
            return f"{self.price:,.0f} تومان"
        else:
            if self.deposit and self.rent:
                return f"ودیعه: {self.deposit:,.0f} - اجاره: {self.rent:,.0f}"
            return f"{self.price:,.0f} تومان"

    def get_floor_display(self):
        """نمایش طبقه به صورت خوانا"""
        if self.floor is None:
            return 'نامشخص'
        floor_map = {
            0: 'همکف',
            -1: 'زیرزمین',
        }
        if self.floor in floor_map:
            return floor_map[self.floor]
        return f"طبقه {self.floor}"

    @property
    def has_all_images(self):
        """بررسی اینکه آیا همه تصاویر وجود دارند"""
        return all([self.image, self.image_2, self.image_3, self.image_4])

    def increase_views(self):
        """افزایش تعداد بازدید"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
