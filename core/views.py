from django.shortcuts import render, get_object_or_404
from properties.models import Property
from team.models import TeamMember

def home(request):
    # دریافت ۴ ملک ویژه (آخرین ملک‌های منتشرشده)
    properties = Property.objects.filter(is_published=True)[:4]
    # دریافت ۲ عضو تیم برای نمایش در صفحه اصلی
    team_members = TeamMember.objects.filter(is_active=True)[:2]
    
    context = {
        'properties': properties,
        'team_members': team_members,
    }
    return render(request, 'core/home.html', context)

def property_list(request):
    # دریافت پارامترهای فیلتر از GET
    transaction_type = request.GET.get('transaction_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # شروع با همه ملک‌های منتشرشده
    properties = Property.objects.filter(is_published=True)
    
    # اعمال فیلترها
    if transaction_type:
        properties = properties.filter(transaction_type=transaction_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # اگر درخواست HTMX باشد، فقط لیست ملک‌ها را برمی‌گردانیم
    if request.htmx:
        return render(request, 'core/partials/property_list_partial.html', {'properties': properties})
    
    # در غیر این صورت، صفحه کامل را نمایش بده
    context = {
        'properties': properties,
        'transaction_type': transaction_type,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'core/property_list.html', context)

def property_detail(request, slug):
    """
    نمایش جزئیات یک ملک بر اساس slug
    """
    # دریافت ملک با اسلاگ یا خطای 404 اگر وجود نداشت
    property = get_object_or_404(Property, slug=slug, is_published=True)
    
    context = {
        'property': property,
    }
    return render(request, 'core/property_detail.html', context)
