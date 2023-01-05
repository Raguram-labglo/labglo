import http,json, re
import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render


def get_meta_redirect(content):
    soup  = BeautifulSoup(content)
    result=soup.find("meta",attrs={"http-equiv":"refresh"})
    if result:
        refresh_content = result['content']
        print ("refresh_content", refresh_content)
        url = refresh_content.partition('=')[2]
        if url:
            url=url.replace("'", "")
            return url
    try:
        # sometime we get redirect as html onload
        script = soup.find('script').get_text()
        match = re.search('store_link = "(?P<url>.+)";', script)
        if not match:
            match = re.search('window.location="(?P<url>.+)"', script)
        if match:
            url = match.group('url')
        if url:
            print ("Found URL throught OnLoad", url)
            return url
    except Exception as e:
        print (e)
        """wait,text=result["content"].split(";")
        if text.strip().lower().startswith("url="):
            url=text[4:].replace("'", "")
            return url"""
    return None

def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            break


def get_302_url(url, proxies, ua):
    if ua == "ios":
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153"
    if ua == "android":
        user_agent = "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"
    else:
        yield None
    headers = {
        "User-Agent": user_agent}
    while True:
        yield url
        if not url or not url.startswith("http"):
            print ("BREAKING", url)
            break
        response = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies)
        print ("response.status_code", response.status_code)
        urls = []
        if response.status_code in [301, 302, 303]:
            url = response.headers['Location']
        if response.status_code == 200:
            url = get_meta_redirect(response.content)


def get_request_direct(url):
    http.client.HTTPSConnection.debuglevel = 1  
    req = urllib2.Request(url)  
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36"
    req.add_header("Accept", "text/html,*/*")  
    req.add_header("Connection", "Keep-Alive")
    req.add_header("User-Agent", user_agent) 
    op = urllib2.build_opener()
    try:
        resp = op.open(req)
    except urllib2.HTTPError as err:
        if err.code == 302:
            urls = []
            for u in get_302_url(url):
                urls.append(u)
            return urls, False
        return None
    print ("resp", resp.getcode())
    if resp.getcode() == 200:
        meta_redirect_url = get_meta_redirect(resp.read())
        print ("meta_redirect_url", meta_redirect_url)
        if meta_redirect_url:
            return [meta_redirect_url], True
    return [resp.url], False


def get_all_redirect_url(request):
    if request.method == "GET":
        return render(request, 'bola.html')
    print ("asds")
    url = request.POST.get("url", '')
    country_code = request.POST.get("country", "")
    ua = request.POST.get("ua", "").strip().lower()

    if not all([url, country_code]):
        return HttpResponse(json.dumps({"error": "Pl pass url and country_code "})
                            , content_type="application/json")
    url = urllib2.unquote(url)
    print ("url", url)
    username = "lum-customer-mobfly-zone-new_residential"
    password = "20k793indmtf"
    port = 22225
    proxies = {'http': 'http://{0}-country-{1}:{2}@zproxy.lum-superproxy.io:{3}'.format(username,
                                                                                        country_code.lower(),
                                                                                        password,
                                                                                        port)}
    proxies['https'] = proxies['http'].replace('http', 'https')
    redirect_urls = []
    for url in get_302_url(url, proxies, ua):
        if url:
            redirect_urls.append(url)
    return render(request, 'bola.html', {'redirect_urls':redirect_urls})


def bola_sample(request):

    url = request.POST.get('url',)
    country = request.POST.get('country',)
    ua =request.POST.get('ua',)
    sample_dict = {}
    sample_dict['url'] = url
    sample_dict['country'] = country
    sample_dict['ua'] = ua


    return render(request, 'bola.html', {'form': sample_dict})
