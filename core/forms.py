import urllib
# import urllib2
import urllib.request as urllib2
import json

from django import forms
from django.conf import settings
from django.utils.translation import gettext as _

from core.models import Lead


class LeadForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Name',
        'class': 'form-control',
        'required': 'required',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Mobile',
        'class': 'form-control',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
        'required': 'required',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Message',
        'class': 'form-control',
        'required': 'required',
    }))
    
    class Meta :
        model = Lead
        fields = ['name', 'phone', 'message', 'email']

    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(LeadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = False
        self.fields['phone'].label = False
        self.fields['email'].label = False
        self.fields['message'].label = False

    def clean(self):
        super(LeadForm, self).clean()
        # test the google recaptcha
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': self.request.POST.get(u'g-recaptcha-response', None),
            'remoteip': self.request.META.get("REMOTE_ADDR", None),
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        # result["success"] will be True on a success
        if not result["success"]:
            raise forms.ValidationError(_(u'Only humans are allowed to submit this form.'))
        return self.cleaned_data


class ProductCrawlForm(forms.Form):
    """
    Form to submit request to crawl product url
    """

    url = forms.URLField(widget=forms.TextInput(attrs={
        'placeholder': 'Product URL',
        'class': 'form-control',
        'required': 'required',
    }))

    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(ProductCrawlForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = False

    def clean(self):
        super(ProductCrawlForm, self).clean()
        # test the google recaptcha
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': self.request.POST.get(u'g-recaptcha-response', None),
            'remoteip': self.request.META.get("REMOTE_ADDR", None),
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        # result["success"] will be True on a success
        if not result["success"]:
            raise forms.ValidationError(_(u'Only humans are allowed to submit this form.'))
        return self.cleaned_data
