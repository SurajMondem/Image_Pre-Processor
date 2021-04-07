from .forms import PhotoForm
from .models import Photo

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages

import json


# Create your views here.


def photo_add_view(request):
    form = PhotoForm(request.POST or None, request.FILES or None)

    if request.is_ajax():
        pic_id = json.loads(request.POST.get('id'))
        action = request.POST.get('action')

        if pic_id is None:
            if form.is_valid():
                obj = form.save(commit=False)
        else:
            obj = Photo.objects.get(id=pic_id)

        obj.action = action
        obj.save()
        data = serializers.serialize('json', [obj])
        return JsonResponse({'data': data})

    context = {
        'form': form,
    }

    return render(request, 'photos/main.html', context)
