from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'transaction_type', 'is_published', 'created_at')
    list_filter = ('transaction_type', 'is_published')
    search_fields = ('title', 'address')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)
