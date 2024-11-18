from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from catalogs.models import ClientStatus, Subscription, DiscoverySource

class Customer(models.Model):
    """Customer model with mandatory fields."""
    client_code = models.CharField(max_length=100, unique=True, blank=False)  
    name = models.CharField(max_length=255, blank=False)  
    curp = models.CharField(max_length=18, unique=True, blank=False)  
    enrollment_date = models.DateField(blank=False)  
    birth_date = models.DateField(blank=False)  
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=gender_choices,
        blank=False,  
    )
    phone_number = models.CharField(max_length=15, blank=False)  
    email = models.EmailField(blank=False)  
    photo = models.ImageField(upload_to='customers_photos/', blank=False)    
    how_did_you_hear = models.ForeignKey(DiscoverySource, on_delete=models.SET_NULL, null=True, blank=False, related_name='customer_sources')  # Relación con DiscoverySource
    how_did_you_hear_details = models.TextField(blank=True, null=True)  # Detalles adicionales de cómo se enteraron
    subscriptions = models.ManyToManyField(Subscription, related_name='customers', blank=True)
    # Campos booleanos para condiciones de salud
    has_illness = models.BooleanField(default=False, blank=False, verbose_name="Padece algún tipo de enfermedad?")
    has_allergy = models.BooleanField(default=False, blank=False, verbose_name="Padece alguna alergia?")
    has_flat_feet = models.BooleanField(default=False, blank=False, verbose_name="Tiene pie plano?")
    has_heart_conditions = models.BooleanField(default=False, blank=False, verbose_name="Tiene problemas cardiacos?")

    def __str__(self):
        return self.name


class CustomerContact(models.Model):
    """Model to represent a contact for a customer."""
    customer = models.ForeignKey(
        Customer, related_name='contacts', on_delete=models.CASCADE, blank=False
    )  
    name = models.CharField(max_length=255, blank=False)  
    phone_number = models.CharField(max_length=15, blank=False)  
    relation = models.CharField(max_length=100, blank=False)  
    is_primary = models.BooleanField(default=False, blank=False)  
    is_emergency = models.BooleanField(default=False, blank=False)  

    def clean(self):
        """Validaciones personalizadas para asegurarse de que haya un único contacto principal y de emergencia."""
        
        # Validar que solo haya un contacto principal y uno de emergencia
        primary_contacts = self.customer.contacts.filter(is_primary=True)
        emergency_contacts = self.customer.contacts.filter(is_emergency=True)
        
        if self.is_primary and primary_contacts.exists():
            raise ValidationError("There can only be one primary contact. Please remove the primary flag from another contact.")
        
        if self.is_emergency and emergency_contacts.exists():
            raise ValidationError("There can only be one emergency contact. Please remove the emergency flag from another contact.")

        # Asegurarse de que haya al menos un contacto principal y uno de emergencia
        if not self.customer.contacts.filter(is_primary=True).exists():
            raise ValidationError("At least one contact must be marked as the primary contact.")
        if not self.customer.contacts.filter(is_emergency=True).exists():
            raise ValidationError("At least one contact must be marked as the emergency contact.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a la validación personalizada antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class CustomerStatus(models.Model):
    """Model to represent the status of a customer."""
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='statuses', null=False, blank=False)  # Relación con el modelo Customer
    status = models.ForeignKey(ClientStatus, on_delete=models.CASCADE, related_name='customer_statuses', null=False, blank=False)  # Relación con ClientStatus
    reason = models.TextField(blank=False, null=False)  # Razón para el cambio de estado
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_changed = models.DateTimeField(auto_now_add=True, null=False, blank=False)  # Fecha y hora del cambio de estado

    def __str__(self):
        return f"{self.customer.name} - {self.status.name} - {self.date_changed}"

    class Meta:
        # No permitir la modificación de un status ya existente
        unique_together = ('customer', 'status', 'date_changed')

    def save(self, *args, **kwargs):
        """Override save method to enforce non-modifiable status."""
        if self.pk is not None:  # Si ya existe una instancia
            raise ValidationError("Cannot modify an existing status. You can only add new statuses.")
        
        super().save(*args, **kwargs)
