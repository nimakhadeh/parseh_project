from django.shortcuts import render
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
    # دریافت همه ملک‌های منتشرشده با صفحه‌بندی
    properties_list = Property.objects.filter(is_published=True)
    
    context = {
        'properties': properties_list,
    }
    return render(request, 'core/property_list.html', context)