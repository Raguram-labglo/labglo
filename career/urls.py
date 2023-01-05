from django.urls import re_path as url
from career.views import (JobsList, submit_resume, DriveListView, DriveDetailsView,
    drive_registration, ConfirmCandidatesList, DriveSlotCreateView, DriveTimeSlotList)

app_name = 'career'
urlpatterns = [
    url(r'^$', JobsList.as_view(), name='jobs_list'),

    url(r'^submit/resume/$', submit_resume, name='submit_resume'),

    url(r'^(?P<slug>[-\w]+)/apply/$', submit_resume, name='apply_post'),

    url(r'^drives/$', DriveListView.as_view(), name='drive_home'),

    url(r'^drive/details/(?P<slug>[\w-]+)/$', DriveDetailsView.as_view(),name='drive_details'),

    url(r'^drive/registration/(?P<slug>[\w-]+)/$', drive_registration, name='drive_registration'),

    url(r'^confirmed/candidates/$', ConfirmCandidatesList.as_view(), name='confirmed_candidated'),

    url(r'^confirm/timeslot/$', DriveSlotCreateView.as_view(), name='confirmed_timeslot'),

    url(r'^time-slots/$', DriveTimeSlotList.as_view(), name='time_slot_list'),

]
