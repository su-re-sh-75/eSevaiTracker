from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Application, ServiceCategory, Service, Payment, SubmittedDocument
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError

@login_required(login_url='/users/login/')
def new_application(request):
    categories = ServiceCategory.objects.prefetch_related('services')
    preselected_cat_id = request.GET.get('category', 1)
    preselected_category = ServiceCategory.objects.get(id=preselected_cat_id)
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            service_id = request.POST.get('service')
            transaction_id = request.POST.get('transactionID')
            screenshot = request.FILES.get('paymentScreenshot')
            docs = request.FILES.getlist('docs')

            service = Service.objects.get(id=service_id)

            if Payment.objects.filter(transactionID=transaction_id).exists():
                messages.error(request, "This UPI Transaction ID has already been used. Application not submitted.")
                return redirect('iniyathalaimurai:new_application')

            payment = Payment.objects.create(
                transactionID=transaction_id,
                customer=request.user,
                service=service,
                amount=service.price,
                status='verifying',
                screenshot=screenshot
            )

            application = Application.objects.create(
                customer=request.user,
                service=service,
                status='processing',
                applicationID=f'APP-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                payment=payment
            )

            for doc in docs:
                SubmittedDocument.objects.create(application=application, file=doc)

            messages.success(request, f"Application for {application.service} is submitted successfully.")
            return redirect('iniyathalaimurai:new_application')

        except IntegrityError as e:
            print("IntegrityError during application/payment creation:", e)
            messages.error(request, "Something went wrong while submitting your application. Please try again.")

        except Exception as e:
            print("Unexpected error:", e)
            messages.error(request, "An unexpected error occurred. Please try again or contact support.")

    return render(request, 'iniyathalaimurai/new_application.html', {
        'categories': categories,
        'preselected_cat_id': preselected_cat_id,
        'preselected_category': preselected_category,
    })

@login_required(login_url="/users/login/")
def user_applications(request):
    categories = ServiceCategory.objects.prefetch_related('services')

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
        'page_obj': page_obj,
        'categories': categories,
    })

@login_required(login_url="/users/login/")
def user_payments(request):
    categories = ServiceCategory.objects.prefetch_related('services')

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
        'page_obj': page_obj,
        'categories': categories,
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
            'image_url': category.image.url,
            'application_count': application_count
        })

    recent_applications = Application.objects.filter(customer=user).select_related('service', 'service__category').order_by('-userAppliedAt')[:10]

    context = {
        'service_data': service_data,
        'recent_applications': recent_applications,
        'categories': categories,
    }
    return render(request, 'iniyathalaimurai/user_dashboard.html', context)

@login_required(login_url="/users/login/")
def staff_dashboard(request):
    categories = ServiceCategory.objects.prefetch_related('services')

    context = {
        'categories': categories,
    }
    return render(request, "iniyathalaimurai/staff_dashboard.html", context)
