from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Skill(models.Model):
    """Model to list out all skills"""
    skill_name = models.CharField(max_length=252)           # Skills added by admin
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.skill_name

class JobListing(models.Model):
    """Model to save all openings in organisation"""
    is_active = models.BooleanField(default=True)           # To check is job expired or not
    job_code = models.CharField(unique=True, max_length=10)
    job_title = models.CharField(max_length=254)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    job_description = RichTextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='required_skills')
    required_qualification = models.CharField(max_length=254, blank=True, null=True)
    is_fresher = models.BooleanField(default=False)
    min_exp = models.PositiveSmallIntegerField(blank=True, null=True)
    max_exp = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=125, blank=True, null=True)
    posting_date = models.DateTimeField(blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    reference_link = models.URLField(max_length=512, blank=True, null=True)
    contact_email = models.EmailField(max_length=254, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse("career:apply_post", kwargs={'slug':self.slug})

class Candidate(models.Model):
    """ Model to save the details of candidates who are submitted
    their profiles or applied for positions.
    """
    MALE = 0
    FEMALE = 1
    OTHER = 2
    GENDER_CHOICES = ( 
        (MALE, 'Male'), 
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    first_name = models.CharField(max_length=252)
    last_name = models.CharField(max_length=252)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    current_company = models.CharField(max_length=125, blank=True, null=True)
    current_location = models.CharField(max_length=125, blank=True, null=True)
    total_exp = models.PositiveSmallIntegerField(blank=True, null=True)
    relevant_exp = models.PositiveSmallIntegerField(blank=True, null=True)
    current_ctc = models.PositiveIntegerField(blank=True, null=True)
    expected_ctc = models.PositiveIntegerField(blank=True, null=True)
    resume = models.FileField(upload_to='candidate_resumes')
    notice_period = models.PositiveSmallIntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_notified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.first_name

    def resume_link(self):
        if self.resume:
            return "<a href='%s' target='_new'>download</a>" % (self.resume.url,)
        else:
            return "No attachment"

    resume_link.allow_tags = True

class Applicant(models.Model):
    """ To save the job post with applied candidate profile """
    candidate = models.ForeignKey(Candidate, related_name='candidate_profile', on_delete=models.CASCADE) # Pointing to candidate profile
    job_listing = models.ForeignKey(JobListing, related_name='job_listing', on_delete=models.CASCADE) # Pointing to Job position
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.candidate.first_name

class TempCandidate(Candidate):
    job_listing = models.ForeignKey(JobListing, blank=True, null=True, on_delete=models.CASCADE)
    verification_key = models.UUIDField(unique=True, db_index=True)

class Drive(models.Model):
    """ To save the placement drives details """
    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512, unique=True, db_index=True)
    description = RichTextField(blank=True, null=True)
    from_date = models.DateTimeField(default=timezone.now, editable=True)
    to_date = models.DateTimeField(default=timezone.now, editable=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    last_date_to_apply = models.DateTimeField(default=timezone.now, editable=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("career:drive_details", kwargs={'slug':self.slug})

class DriveRegistration(models.Model):
    """ To save registration details for drive """
    first_name = models.CharField(max_length=252)
    last_name = models.CharField(max_length=252)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=256)
    course = models.CharField(max_length=256)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True, null=True)
    college = models.CharField(max_length=512)
    university = models.CharField(max_length=512)
    location = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=512, null=True, blank=True)
    state = models.CharField(max_length=512, null=True, blank=True)
    referred_by = models.CharField(max_length=512, null=True, blank=True)
    address = models.TextField(max_length=512, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('email', 'drive')
        ordering = ('created_on', 'id')

    def __unicode__(self):
        return self.first_name

    def has_confirmed_timeslot(self):
        return DriveTimeSlot.objects.filter(drive_registration=self).exists()


class DriveTimeSlot(models.Model):
    drive_registration = models.OneToOneField(DriveRegistration, on_delete=models.CASCADE)
    slot = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.drive_registration.first_name