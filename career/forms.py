import os
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from career.models import (Skill, JobListing, Candidate, Applicant, Drive, DriveRegistration)
from django.forms import ModelForm


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name',]

class JobListingForm(ModelForm):
    class Meta:
        model = JobListing
        exclude = ['created_on', 'updated_on']

class CandidateForm(ModelForm):
    present_openings = forms.ModelChoiceField(label='PRESENT OPENINGS', queryset=JobListing.objects.all(),
        empty_label="---Current Available Positions---", required = False)
    
    class Meta:
        model = Candidate
        fields = ['present_openings', 'first_name', 'last_name', 'phone', 'email',
        'gender','current_company', 'current_location', 'total_exp', 'relevant_exp',
        'current_ctc', 'expected_ctc', 'notice_period', 'resume']

    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(CandidateForm, self).__init__(*args, **kwargs)

    def clean_total_exp(self):
        try:
            content = self.cleaned_data['total_exp']
        except:
            content = 0
        if content > 250:
            raise forms.ValidationError("Value exceeded.")
        return content

    def clean_relevant_exp(self):
        try:
            content = self.cleaned_data['relevant_exp']
        except:
            content = 250
        if content > 10000000:
            raise forms.ValidationError("Value exceeded.")
        return content

    def clean_current_ctc(self):
        try:
            content = self.cleaned_data['current_ctc']
        except:
            content = 0
        if content > 10000000:
            raise forms.ValidationError("Value exceeded.")
        return content

    def clean_expected_ctc(self):
        try:
            content = self.cleaned_data['expected_ctc']
        except:
            content = 0
        if content > 5000000:
            raise forms.ValidationError("Value exceeded.")
        return content

    def clean_notice_period(self):
        try:
            content = self.cleaned_data['notice_period']
        except:
            content = 0
        if content > 100:
            raise forms.ValidationError("Value exceeded.")
        return content

    def clean_resume(self):
        content = self.cleaned_data['resume']
        # file_type = content.content_type.split('/')[1]
        # if file_type not in ['pdf', 'doc', 'msword', 'docx']:
        if str(content).endswith(('.pdf', '.doc', '.docx')):
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(('Please keep filesize under %s.') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE)))
        else:
            raise forms.ValidationError("Only .pdf, .doc and .docx files allowed.")
        return content

    def fields_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clean(self):
        try:
            total_exprnc = self.cleaned_data['total_exp']
        except:
            total_exprnc = 0
        if total_exprnc >= 6:
            self.fields_required(['current_company', 'relevant_exp',
                'current_ctc', 'expected_ctc','notice_period'])
        return self.cleaned_data

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        exclude = ['created_on', 'updated_on']

class DriveForm(ModelForm):
    class Meta:
        model = Drive
        exclude = ['created_on', 'updated_on']

class DriveRegistrationForm(ModelForm):
    class Meta:
        model = DriveRegistration
        fields = ['first_name', 'last_name', 'mobile', 'email', 'qualification',
            'course', 'percentage', 'grade', 'college', 'university', 'location',
            'city', 'state', 'referred_by', 'address' ]

    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(DriveRegistrationForm, self).__init__(*args, **kwargs)

    def clean_percentage(self):
        try:
            content = self.cleaned_data['percentage']
        except:
            content = 0
        if content > 100 :
            raise forms.ValidationError("Value exceeded.")
        elif content < 0 and content != None :
            raise forms.ValidationError("Please enter the positive value.")
        return content

    # def clean_location(self):
    #     location = self.cleaned_data['location']
    #     if location == None:
    #         raise forms.ValidationError("This field is required.")
    #     else:
    #         return location

    # def clean(self):
    #     city = self.cleaned_data['city']
    #     state = self.cleaned_data['state']
    #     if city == None or state == None:
    #         raise forms.ValidationError({'location':"Please enter correct value"})
    #     return self.cleaned_data