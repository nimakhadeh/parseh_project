from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='نامک')
    content = models.TextField(verbose_name='محتوا')
    summary = models.TextField(max_length=300, verbose_name='خلاصه')
    image = models.ImageField(upload_to='blog/', verbose_name='تصویر شاخص')
    tags = models.CharField(max_length=200, blank=True, verbose_name='برچسب‌ها (با کاما جدا کنید)')
    is_published = models.BooleanField(default=True, verbose_name='منتشر شود؟')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    views_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
