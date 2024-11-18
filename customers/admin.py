from django.contrib import admin
from .models import Customer, CustomerContact, CustomerStatus

# Inline model para los contactos de Customer
class CustomerContactInline(admin.TabularInline):
    model = CustomerContact
    extra = 1
    fields = ('name', 'phone_number', 'relation', 'is_primary', 'is_emergency')
    readonly_fields = ('is_primary', 'is_emergency')

# Inline model para los estados de Customer
class CustomerStatusInline(admin.TabularInline):
    model = CustomerStatus
    extra = 1
    fields = ('status', 'reason', 'changed_by', 'date_changed')
    readonly_fields = ('date_changed',)  # Establecer date_changed como solo lectura

# Configuración del modelo Customer en el admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('client_code', 'name', 'curp', 'email', 'phone_number', 'gender', 'enrollment_date')
    search_fields = ('client_code', 'name', 'curp', 'email')
    list_filter = ('gender', 'has_illness', 'has_allergy')
    ordering = ('client_code',)
    filter_horizontal = ('subscriptions',)
    
    # Agregar los inlines para los contactos y los estados
    inlines = [CustomerContactInline, CustomerStatusInline]

# Registro del modelo CustomerStatus
@admin.register(CustomerStatus)
class CustomerStatusAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'reason', 'date_changed', 'changed_by')
    list_filter = ('status', 'date_changed')
    readonly_fields = ('date_changed',)  # Establecer date_changed como solo lectura

