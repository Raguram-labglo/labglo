from django.contrib import admin
from core.models import Lead

# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['name', 'phone', 'email',
        	'message', 'remarks']})
    ]
    
    list_display = ('name','phone', 'email', 'message','remarks',
        'created_on', 'updated_on')
    
    search_fields = ["name"]

admin.site.register(Lead, LeadAdmin)