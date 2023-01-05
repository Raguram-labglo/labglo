import base64
import urllib
from urllib.parse import urlparse
#import diffbot
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from core.models import Lead
from core.forms import LeadForm, ProductCrawlForm


def contact(request):
    if request.method == "POST":
        form = LeadForm(request.POST, request=request)
        if form.is_valid():
            fm_name = request.POST['name']
            fm_phone = request.POST['phone']
            fm_email = request.POST['email']
            fm_message = request.POST['message']
            obj = Lead.objects.create(name=fm_name, phone=fm_phone,
                email=fm_email, message=fm_message)
            subject = "LABGLO - New contact form submission"
            greetings = 'Hello Team,' + '\n' + 'Please check the below details and get back as soon as possible.' + '\n'
            body = greetings + '\n Name: {} \n Mobile: {} \n Email: {} \n Massage:{}'.format(
                fm_name, fm_phone, fm_email, fm_message)
            recipients = ['info@labglo.com']
            send_mail(subject, body, settings.EMAIL_HOST_USER, recipients)
            return JsonResponse({
                    'status':'Success! Thank you for contact, our team will get back you soon.'
                })
        else:
            return JsonResponse({'foo': form.errors})
    else:
        form = LeadForm()
        return render(request, 'contact_us.html', {'form':form})


def uri_encode_decode(request):
    code_val = request.GET.get('code_val')
    action = request.GET.get('action')
    input_txt = request.GET.get('input_txt')
    response = ''
    try:
        if input_txt != '' and input_txt is not None:
            if code_val == "Base64":
                if action == "Encode":
                    response = base64.b64encode(input_txt)
                elif action == "Decode":
                    response = base64.b64decode(input_txt)
        return JsonResponse({'result': response})
    except:
        return JsonResponse({'error': "Please enter the correct value to decode."})


def amazon_affiliate(request):
    '''
    :return: a url with a tag labglophase3-20
    '''

    text_value = request.POST.get('textbox-value')
    try:
        if text_value != '':
            u = urlparse.urlparse(text_value)
            query = urlparse.parse_qs(u.query)
            query['tag'] = 'labglophase3-20'
            u = u._replace(query=urllib.urlencode(query, True))
            url = urlparse.urlunparse(u)
        else:
            url = ''
    except:
        url = ''
    return render(request, 'sample.html', {'form': url})


def product_crawl(request):
    """
    Method to crawl the details of product and giving response as Json.
    """

    if request.method == "POST":
        form = ProductCrawlForm(request.POST, request=request)
        if form.is_valid():
            fm_url = request.POST['url']
            client = diffbot.Client(token=settings.DEVELOPER_TOKEN)
            response = client.product(url=fm_url, timeout=90000)
            data = {}
            if 'request' in response.keys() and 'pageUrl' in response['request'].keys() and response['request']['pageUrl']:
                data['url'] = str(response['request']['pageUrl'])

            if 'objects' in response.keys():
                objects = response['objects'][0]

                if 'title' in objects.keys() and objects['title']:
                    data['title'] = str(objects['title'])

                if 'productId' in objects.keys() and objects['productId']:
                    data['product_id'] = str(objects['productId'])

                if 'type' in objects.keys() and objects['type']:
                    data['type'] = str(objects['type'])

                if 'category' in objects.keys() and objects['category']:
                    data['category'] = str(objects['category'])

                if 'regularPrice' in objects.keys() and objects['regularPrice']:
                    data['price'] = str(objects['regularPrice'])

                if 'offerPrice' in objects.keys() and objects['offerPrice']:
                    data['offer_price'] = str(objects['offerPrice'])

                if 'availability' in objects.keys() and objects['availability']:
                    data['availability'] = str(objects['availability'])

                if 'sku' in objects.keys() and objects['sku']:
                    data['sku'] = str(objects['sku'])

                if 'humanLanguage' in objects.keys() and objects['humanLanguage']:
                    data['language'] = str(objects['humanLanguage'])

                if 'text' in objects.keys() and objects['text']:
                    data['description'] = str(objects['text'].encode("utf-8"))

                data['specifications'] = {}
                include_specs_fields = ["color", "product_dimensions", "shape", "package_contents"]
                if 'specs' in objects.keys() and objects['specs']:
                    for key in objects['specs'].keys():
                        if str(key) in include_specs_fields:
                            data['specifications'][str(key)] = str(objects['specs'][key])

                data['images'] = []
                include_img_fields = ["url"]
                if 'images' in objects.keys() and objects['images']:
                    for itm in objects['images']:
                        img = {}
                        for key in itm.keys():
                            if str(key) in include_img_fields:
                                img[str(key)] = itm[key] if isinstance(itm[key], int) else str(itm[key])
                        data['images'].append(img)
            if data:
                return JsonResponse({'response': data})
            else:
                return JsonResponse({'response': "The Product not found."})
        else:
            return JsonResponse({'errors': form.errors})
    else:
        form = ProductCrawlForm()
        return render(request, 'product_crawl.html', {'form': form})
