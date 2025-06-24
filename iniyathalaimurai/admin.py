from django.contrib import admin
from .models import ServiceCategory, Service, Application, Payment, SubmittedDocument

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price']
    list_filter = ['category']
    search_fields = ['name', 'category__name']
    ordering = ['category', 'name', 'price']

class SubmittedDocumentInline(admin.TabularInline):
    model = SubmittedDocument
    extra = 0
    readonly_fields = ['file']
    fields = ['file']
    can_delete = True

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'acknowledgementNumber', 'customer', 'service', 'status', 'payment__amount',
        'userAppliedAt', 'applicationAppliedAt',
    ]
    list_filter = ['status', 'service__category']
    search_fields = ['customer__phone_num', 'service__name']
    autocomplete_fields = ['customer', 'service', 'payment']
    date_hierarchy = 'userAppliedAt'
    ordering = ['-userAppliedAt']
    inlines = [SubmittedDocumentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'transactionID', 'customer', 'service', 'amount', 'status', 'paidAt', 'screenshot']
    list_filter = ['status', 'service__category']
    search_fields = ['customer__phone_num', 'service__name']
    autocomplete_fields = ['customer', 'service']
    date_hierarchy = 'paidAt'
    ordering = ['-paidAt']


