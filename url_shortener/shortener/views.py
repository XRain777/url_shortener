from django.db.models import F
from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from shortener.models import Link

from url_normalize import url_normalize

import json

def index(request):
    return render(request, 'index.html')

@require_POST
def create(request):
    request_json = json.loads(request.body.decode('utf-8'))
    print(request_json)
    if 'url' in request_json and len(request_json['url'].strip()) > 0:
        val = URLValidator()
        try:
            long_url = url_normalize(request_json['url'].strip())
            val(long_url)
            existing_link = Link.objects.filter(url=long_url)
            if existing_link.count() == 0:
                link = Link(url=long_url, date_created=timezone.now())
                link.save()
            else:
                link = existing_link[0]
            return JsonResponse({'short_url': request.build_absolute_uri(reverse('shortener:goto', args=[link.short_url()]))})
        except ValidationError:
            return JsonResponse({'error': 'URL is not valid.'}, status=400)
    else:
        return JsonResponse({'error': 'No URL given.'}, status=400)

@require_GET
def goto(request, shorturl):
    links = Link.objects.have_short_url(shorturl)
    if links.count() == 0:
        return HttpResponse('Short URL doesn\'t exist.', status=404)
    link = links[0]
    link.click_count = F('click_count') + 1
    link.save()
    return HttpResponseRedirect(link.url)

@require_GET
def stats(request, shorturl):
    links = Link.objects.have_short_url(shorturl)
    if links.count() == 0:
        return HttpResponse('Short URL doesn\t exist.', status=404)
    link = links[0]
    context = { 'long_url': link.url, 'short_url': request.build_absolute_uri(reverse('shortener:goto', args=([link.short_url()]))), 'click_count': link.click_count, 'date_created': link.date_created }
    return JsonResponse(context)

@require_GET
def qrcode(request, shorturl):
    links = Link.objects.have_short_url(shorturl)
    if links.count() == 0:
        return HttpResponse('Short URL doesn\t exist.', status=404)
    link = links[0]
    context = { 'short_url': request.build_absolute_uri(reverse('shortener:goto', args=([link.short_url()])))}
    return render(request, 'qr.html', context=context)
