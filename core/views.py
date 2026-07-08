from django.shortcuts import render, get_object_or_404
from properties.models import Property
from team.models import TeamMember

def home(request):
    # فقط ملک‌هایی که slug دارند و منتشر شده‌اند
    properties = Property.objects.filter(is_published=True).exclude(slug='')[:4]
    team_members = TeamMember.objects.filter(is_active=True)[:2]
    
    context = {
        'properties': properties,
        'team_members': team_members,
    }
    return render(request, 'core/home.html', context)

def property_list(request):
    transaction_type = request.GET.get('transaction_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # فقط ملک‌هایی که slug دارند
    properties = Property.objects.filter(is_published=True).exclude(slug='')
    
    if transaction_type:
        properties = properties.filter(transaction_type=transaction_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    if request.htmx:
        return render(request, 'core/partials/property_list_partial.html', {'properties': properties})
    
    context = {
        'properties': properties,
        'transaction_type': transaction_type,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'core/property_list.html', context)

def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug, is_published=True)
    context = {
        'property': property,
    }
    return render(request, 'core/property_detail.html', context)
