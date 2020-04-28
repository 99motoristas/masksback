from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from mask.models import Driver
from django.db.models import Q
import csv

def index(request):
    return render(request, 'mask/index.html')

def find_phone_cpf(request, cpf_or_phone):
    # Driver.objects.create(author=me, title='Sample title', text='Test')
    print(cpf_or_phone)
    driver = Driver.objects.filter(hashed_cpf=cpf_or_phone).first()
    print(driver)
    if not driver:
        driver = Driver.objects.filter(hashed_phone=cpf_or_phone).first()
    if not driver:
        return JsonResponse({'result':'false'})

    return JsonResponse({'result': 'true',
                         'date': driver.date})

def confirm_picking_mask(request, cpf_or_phone, timestamp):
    if request.method == 'POST':
        driver = Driver.objects.filter(Q(hashed_cpf=cpf_or_phone) | Q(hashed_phone=cpf_or_phone)).first()
        if not driver:
            return JsonResponse({'result': 'false'})
        driver.date = timestamp
        driver.save()
        return JsonResponse({'result': 'true'})

def get_driver_status(request, city, picked_up_flag):

    if picked_up_flag == "1":
        if city == "all":
            drivers = Driver.objects.filter(~Q(date="0"))
        else:
            drivers = Driver.objects.filter(city=city).exclude(date="0")
    else:
        if city == "all":
            drivers = Driver.objects.filter(date="0")
        else:
            drivers = Driver.objects.filter(city=city, date="0")

    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['HashedPhone', 'HashedCPF', 'Date', 'City'])
    for driver in drivers:
        output.append([driver.hashed_phone, driver.hashed_cpf, driver.date, driver.city])
    #CSV Data
    writer.writerows(output)
    return response
