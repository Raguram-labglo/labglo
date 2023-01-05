from django.urls import re_path as url
from django.views.generic import TemplateView

from core.redirect import get_all_redirect_url, bola_sample
from core.views import contact, uri_encode_decode, amazon_affiliate, product_crawl

app_name = 'core'
urlpatterns = [
    # app urls
    url(r'^contact/$', contact, name='contact'),
    url(r'^product-crawl/$', product_crawl, name='product_crawl'),
    url(r'^coded/encryption/$', uri_encode_decode, name='coded_encryption'),
    url(r'^test/redirect/$', get_all_redirect_url, name='get_all_redirect_url'),
    url(r'^bola/$', bola_sample, name='bola'),
    url(r'^amazon-affiliate/$', amazon_affiliate, name='amazon-affiliate'),

    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^about-us/$', TemplateView.as_view(template_name="about_us.html"), name='about_us'),
    url(r'^services/$', TemplateView.as_view(template_name="services.html"), name='services'),
    url(r'^gallery/$', TemplateView.as_view(template_name="gallery.html"), name='gallery'),
    url(r'^url-encode-decode/$', TemplateView.as_view(template_name="url_encode_decode.html"), name='url_encode_decode'),
    url(r'^mdfaofficial/$', TemplateView.as_view(template_name="thirdpartysite.html"), name='mdfaofficial'),

]




