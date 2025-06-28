from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application, ServiceCategory, Service, Payment, SubmittedDocument
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError
from users.models import User
from django.views.decorators.http import require_POST

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
            'id': category.id,
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

    return render(request, "iniyathalaimurai/staff_dashboard.html")


@login_required(login_url="/users/login/")
def new_customer(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        name = request.POST.get('name')

        if User.objects.filter(phone_num=phone_num).exists():
            messages.error(request, 'Phone number already registered.')
        else:
            user = User.objects.create_user(phone_num=phone_num, name=name, password=password)
            user.is_staff = False
            user.save()
            messages.success(request, f'{user.phone_num} account created successfully!')
            return redirect('iniyathalaimurai:new_customer')
    return render(request, 'iniyathalaimurai/new_customer.html')


@login_required(login_url="/users/login/")
def manage_customers(request):
    customers_list = User.objects.filter(is_staff=False).order_by('-id')

    # customers_list = User.objects.filter(groups__name='Customer').order_by('-id')

    paginator = Paginator(customers_list, 10) 
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'iniyathalaimurai/customers.html', {
        'page_obj': page_obj,
    })

@login_required(login_url="/users/login/")
def delete_customer(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    customer.delete()
    messages.success(request, f"Customer '{customer.phone_num}' deleted successfully.")
    return redirect('iniyathalaimurai:manage_customers')

@login_required(login_url="/users/login/")
def deactivate_customer(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    if customer.is_active:
        customer.is_active = False
        customer.save()
        messages.success(request, f"Customer '{customer.phone_num}' deactivated.")
    return redirect('iniyathalaimurai:manage_customers')

@login_required(login_url="/users/login/")
def activate_customer(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    if not customer.is_active:
        customer.is_active = True
        customer.save()
        messages.success(request, f"Customer '{customer.phone_num}' activated.")
    return redirect('iniyathalaimurai:manage_customers')


@login_required(login_url="/users/login/")
def edit_customer(request, user_id):
    customer = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        name = request.POST.get('name')
        status = request.POST.get('status')

        updated = False
        if phone_num and phone_num != customer.phone_num:
            customer.phone_num = phone_num
            updated = True

        if name and name != customer.name:
            customer.name = name
            updated = True

        if status in ['active', 'inactive']:
            new_status = True if status == 'active' else False
            if customer.is_active != new_status:
                customer.is_active = new_status
                updated = True

        if updated:
            customer.save()
            messages.success(request, f'Customer {customer.phone_num} updated successfully!')
        else:
            messages.info(request, f'No changes made for {customer.phone_num}')

        return redirect('iniyathalaimurai:manage_customers')

    return render(request, 'iniyathalaimurai/edit_customer.html', {
        'customer': customer
    })

@login_required(login_url='/users/login/')
def manage_payments(request):
    payments_list = Payment.objects.select_related('customer', 'service', 'service__category').order_by('-paidAt')

    paginator = Paginator(payments_list, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'iniyathalaimurai/manage_payments.html', {
        'page_obj': page_obj
    })

@require_POST
@login_required(login_url='/users/login/')
def update_payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    new_status = request.POST.get('status')

    if new_status in dict(Payment.STATUS_CHOICES):
        payment.status = new_status
        payment.save()
        messages.success(request, f'Payment #{payment.transactionID} status updated to {new_status}.')
    else:
        messages.error(request, 'Invalid status.')

    return redirect('iniyathalaimurai:manage_payments')

@login_required(login_url='/users/login/')
def manage_applications(request):
    applications = Application.objects.select_related('customer', 'service', 'service__category').order_by('-userAppliedAt')

    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'iniyathalaimurai/manage_applications.html', {
        'page_obj': page_obj
    })

@login_required(login_url='/users/login/')
def upload_certificate(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == 'POST' and request.FILES.get('certificate'):
        application.certificate = request.FILES['certificate']
        application.save()
        messages.success(request, f'{application.customer.phone_num}\'s Certificate uploaded successfully.')
        return redirect('iniyathalaimurai:manage_applications')

    return render(request, 'iniyathalaimurai/upload_certificate.html', {
        'application': application
    })

@require_POST
@login_required(login_url='/users/login/')
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    new_status = request.POST.get('status')

    allowed_statuses = ['processing', 'accepted', 'rejected']

    if new_status in allowed_statuses:
        application.status = new_status
        application.save()
        messages.success(request, f'Application #{application.id} status updated to {new_status}.')
    else:
        messages.error(request, 'Invalid status selected.')

    return redirect('iniyathalaimurai:manage_applications')

@login_required(login_url='/users/login/')
def update_acknowledgement(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.method == 'POST':
        new_ack = request.POST.get('acknowledgementNumber', '').strip()
        application.acknowledgementNumber = new_ack
        application.save()
        messages.success(request, 'Acknowledgement Number updated!')

    return redirect('iniyathalaimurai:manage_applications')
