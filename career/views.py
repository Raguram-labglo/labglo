import os
import logging
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from labglo_site import settings
from labglo_site.helpers import email_notification
from career.models import Skill, JobListing, Candidate, Applicant, Drive, DriveRegistration, DriveTimeSlot
from career.forms import (SkillForm, JobListingForm, CandidateForm, DriveForm, DriveRegistrationForm)

logger = logging.getLogger(__name__)


class JobsList(generic.ListView):
    model = JobListing
    template_name = 'career/careers.html'
    paginate_by = 3

    def get_queryset(self):
        qset = JobListing.objects.filter(is_active=True).order_by("-created_on")
        return qset

def submit_resume(request, slug=None):
    if slug:
        try:
            job_post = JobListing.objects.get(slug=slug)
        except JobListing.DoesNotExist:
            return redirect(reverse("career:submit_resume"))
    else:
        job_post = None
    
    try:
        if request.method == "POST":
            form = CandidateForm(request.POST, request.FILES)
            if form.is_valid():
                cn_email = request.POST.get('email')
                try:
                    obj = Candidate.objects.get(email=cn_email)
                    candidate_form = CandidateForm(request.POST, request.FILES, instance=obj)
                except:
                    candidate_form = CandidateForm(request.POST, request.FILES)
                if candidate_form.is_valid():
                    cn_obj = candidate_form.save(commit=False)
                    cn_obj.save()
                    #If post selected then save application
                    post_name = "Resume submission"
                    post_id = request.POST['present_openings']
                    if post_id != "":
                        post_obj = JobListing.objects.get(id=post_id)
                        post_name = post_obj.job_title
                        obj1, created = Applicant.objects.get_or_create(candidate=cn_obj, job_listing=post_obj)
                        obj1.save()
                    # Send acknowledgement to candidate and admin
                    cn_gender = int(request.POST.get('gender'))
                    cn_name = request.POST.get('first_name')
                    if cn_gender == 0:
                        prefix = "Mr."
                    elif cn_gender == 1:
                        prefix = "Ms."
                    else:
                        prefix = ""
                    context_data = {
                        "candidate_obj" : cn_obj,
                        "candidate_name" : cn_name,
                        "post_name" : post_name,
                        "prefix" : prefix,
                    }
                    email_notification(notify_to='candidate', context_data=context_data)
                    email_notification(notify_to='admin', context_data=context_data)
                    return JsonResponse({
                        'status':"We appreciate your interest in Labglo. \
                        In the event that we wish to arrange a personal interview, \
                        we will contact you by mail or phone."
                    })
                else:
                    return JsonResponse({'foo': candidate_form.errors})
            else:
                return JsonResponse({'foo': form.errors})
        else:
            form = CandidateForm()
            return render(request, 'career/submit_resume.html', {'form':form, 'job_post': job_post})
    except Exception as e:
        logger.warning(str(e))
        logger.error("set_password:%s"%str(e))
        return JsonResponse({'foo': e})


class DriveListView(generic.ListView):
    model = Drive
    template_name = 'career/drives.html'
    paginate_by = 5

    def get_queryset(self):
        qset = Drive.objects.filter(is_active=True).order_by("-created_on")
        return qset

class DriveDetailsView(generic.DetailView):
    model = Drive
    template_name = 'career/drive_details.html'
    context_object_name = 'drive_obj'

    def get_object(self):
        obj = get_object_or_404(Drive, slug=self.kwargs['slug'], is_active=True)
        return obj

def drive_registration(request, slug=None):
    if slug:
        try:
            drive_obj = Drive.objects.get(slug=slug)
        except Drive.DoesNotExist:
            return redirect(reverse("career:drive_home"))
        if request.method == "POST":
            form = DriveRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    user_registration_obj = form.save(commit=False)
                    user_registration_obj.drive = drive_obj
                    user_registration_obj.save()
                    context_data = {"user_obj":user_registration_obj,}
                    email_notification(notify_to='drive_application_received', context_data=context_data)
                    return JsonResponse({
                        'status': "We appreciate your interest in Labglo. \
                        In the event that you selected for drive, \
                        we will contact you by mail or phone."
                    })
                except:
                    return JsonResponse({"error":"Email already registered for this drive."})
            else:
                return JsonResponse({'foo': form.errors})
        else:
            form = DriveRegistrationForm()
            return render(request, 'career/drive_registration.html',
                {'form':form, 'drive_obj': drive_obj, })
    else:
        return redirect(reverse("career:drive_home"))


@method_decorator(login_required(login_url='admin:login'), name='dispatch')
class ConfirmCandidatesList(generic.ListView):
    model = DriveRegistration
    template_name = 'career/confirm_candidates.html'
    context_object_name = "confirm_candidates"

    def get_queryset(self):
        qset = DriveRegistration.objects.filter(is_confirmed=True).order_by("created_on")
        if self.request.GET.get('start_id', None):
            qset = qset.filter(id__gte=self.request.GET.get('start_id'))
        if self.request.GET.get('end_id', None):
            qset = qset.filter(id__lte=self.request.GET.get('end_id'))
        day = self.request.GET.get('day', None)
        if day == 'today':
            t_day = datetime.now()
            qset = qset.filter(updated_on__date=t_day.date())
        return qset

class DriveSlotCreateView(LoginRequiredMixin, View):
    login_url = 'admin:login'
    
    def get(self, request):
        return render(request, 'career/drive_slot_add.html')

    def post(self, request):
        registration_id = self.request.POST.get('field_id', None)
        slot_time = self.request.POST.get('slot_time', None)
        slot_date = self.request.POST.get('slot_date', None)
        if registration_id and slot_time and slot_date:
            drive_registration = get_object_or_404(DriveRegistration, id=registration_id)
            date_time = datetime.strptime('{} {}'.format(slot_date, slot_time), "%Y-%m-%d %H:%M")
            try:
                drive_slot_obj = DriveTimeSlot.objects.create(drive_registration=drive_registration,
                    slot=date_time)
                context = {'message':"Date and Time slot confirmed."}
                data = {"user_obj":drive_registration, "slot_details":date_time}
                email_notification(notify_to='confirm_drive_slot_time', context_data=data)
            except:
                context = {'message':"You already assigned time slot for this id."}
        else:
            context = {'message':"Please check the id and time."}
        return render(request, 'career/drive_slot_add.html', context=context)
        
        
class DriveTimeSlotList(LoginRequiredMixin, generic.ListView):
    login_url = 'admin:login'
    model = DriveTimeSlot
    template_name = 'career/drive-time-slot-list.html'
    context_object_name = 'timeslots'
    
    def get_queryset(self):
        queryset = DriveTimeSlot.objects.all().order_by('drive_registration__id')
        slot_time = self.request.GET.get('slot', None)
        if slot_time:
            try:
                slot_time = datetime.strptime('2017-6-24 {}'.format(slot_time), "%Y-%m-%d %H:%M")
                queryset = queryset.filter(slot=slot_time)
            except:
                pass
        return queryset

