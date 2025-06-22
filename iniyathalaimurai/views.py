from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Application, ServiceCategory, Service, Payment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="/users/login/")
def user_applications(request):
    applications = Application.objects.filter(
        customer=request.user
    ).select_related('service', 'service__category').order_by('-userAppliedAt')

    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'iniyathalaimurai/my_applications.html', {
        'page_obj': page_obj
    })

@login_required(login_url="/users/login/")
def user_payments(request):
    payments = Payment.objects.filter(
        customer=request.user
    ).select_related('service', 'service__category').order_by('-paidAt')

    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'iniyathalaimurai/my_payments.html', {
        'page_obj': page_obj
    })

@login_required(login_url="/users/login/")
def user_dashboard(request):
    user = request.user

    service_data = []

    categories = ServiceCategory.objects.prefetch_related('services')

    for category in categories:
        services = category.services.all()
        
        user_applications = Application.objects.filter(
            customer=user,
            service__in=services
        )
        application_count = user_applications.count()

        service_data.append({
            'category': category.name,
            'image_url': category.image.url if category.image else None,
            'application_count': application_count
        })

    recent_applications = Application.objects.filter(customer=user).select_related('service', 'service__category').order_by('-userAppliedAt')[:10]

    context = {
        'service_data': service_data,
        'recent_applications': recent_applications,
    }
    # print(context)
    return render(request, 'iniyathalaimurai/user_dashboard.html', context)

@login_required(login_url="/users/login/")
def staff_dashboard(request):
    return render(request, "iniyathalaimurai/staff_dashboard.html")
