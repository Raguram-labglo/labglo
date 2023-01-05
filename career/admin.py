from datetime import datetime
from django.contrib import admin
from labglo_site.helpers import email_notification
from career.models import (Skill, JobListing, Candidate, Applicant,
    TempCandidate, Drive, DriveRegistration, DriveTimeSlot)

# Register your models here.
class SkillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['skill_name']})
    ]
    
    list_display = ('skill_name', 'created_on', 'updated_on')
    
    search_fields = ["skill_name"]

class JobListingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['job_code', 'job_title', 'slug', 'is_active', 'is_fresher',
            'job_description',  'skills', 'required_qualification', 'reference_link',
            'min_exp', 'max_exp', 'location', 'posting_date', 'closing_date',
            'contact_email', 'additional_info',]})
    ]
    
    list_display = ('job_code', 'job_title', 'is_active', 'is_fresher',
            'required_qualification', 'min_exp', 'max_exp', 'location',
            'posting_date', 'closing_date', 'contact_email', 'created_on',
            'updated_on')
    
    search_fields = ["job_title"]

    prepopulated_fields = {'slug': ('job_title',), }

    list_filter = ['is_active', 'is_fresher']

class CandidateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['first_name', 'last_name', 'phone', 'email', 'gender',
            'current_company',  'current_location', 'total_exp', 'relevant_exp',
            'current_ctc', 'expected_ctc', 'resume', 'notice_period', 'is_notified']})
    ]
    
    list_display = ('first_name', 'last_name', 'phone', 'email', 'gender',
            'current_company',  'current_location', 'total_exp',
            'relevant_exp', 'current_ctc', 'expected_ctc',
            'notice_period', 'resume_link', 'is_notified',
            'created_on', 'updated_on')
    
    search_fields = ["first_name"]

class ApplicantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['candidate', 'job_listing']})
    ]
    
    list_display = ('candidate', 'job_listing', 'created_on', 'updated_on')
    
    search_fields = ["candidate"]

class DriveAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'slug', 'description', 'from_date',
            'to_date', 'location', 'last_date_to_apply', 'is_active',]})
    ]
    
    list_display = ('title', 'from_date', 'to_date', 'is_active',
            'location', 'created_on', 'updated_on')
    
    search_fields = ["job_title"]

    prepopulated_fields = {'slug': ('title',), }

    list_filter = ['is_active']

class DriveRegistrationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['first_name', 'last_name', 'mobile', 'email',
            'drive', 'qualification', 'course', 'percentage', 'grade',
            'college', 'university', 'location', 'city', 'state',
            'referred_by', 'address', 'is_confirmed']})
    ]
    
    list_display = ('id', 'first_name', 'is_confirmed', 'qualification',
            'course',  'percentage', 'grade', 'college', 'university',
            'city', 'address', 'updated_on')
    
    def mark_confirmed(self, request, queryset):
        rows_updated = queryset.update(is_confirmed=True, updated_on=datetime.now())
        for obj in queryset:
            context_data = {
                'user_obj': obj
            }
            email_notification(notify_to='drive_registration_confirm', context_data=context_data)
        if rows_updated == 1:
            message_bit = "1 registration"
        else:
            message_bit = "%s registrations" % rows_updated
        self.message_user(request, "%s successfully confirmed." % message_bit)

    search_fields = ["first_name", "id"]

    list_filter = ['is_confirmed', 'city', 'state', 'referred_by',]

    actions = [mark_confirmed]

class DriveTimeSlotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['drive_registration', 'slot']})
    ]
    
    list_display = ('drive_registration', 'slot', 'created_on', 'updated_on')

    search_fields = ["drive_registration__id"]


admin.site.register(Skill, SkillAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(TempCandidate)
admin.site.register(Drive, DriveAdmin)
admin.site.register(DriveRegistration, DriveRegistrationAdmin)
admin.site.register(DriveTimeSlot, DriveTimeSlotAdmin)
