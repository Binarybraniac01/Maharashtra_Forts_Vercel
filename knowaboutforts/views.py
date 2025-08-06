from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from home.models import *

@login_required(login_url="/login-page/")
def knowaboutforts(request):
    # For proper pagination
    fort_data = Forts.objects.all()
    paginator = Paginator(fort_data, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Used this bcoz paginaion only takes 9 data set
    all_dist = Forts.objects.values_list('fort_district', flat=True).distinct()
    all_districts = set(all_dist)

    return render(request, "knowaboutforts.html", context={"page_obj":page_obj, "all_districts":all_districts})


@login_required(login_url="/login-page/")
def getdistforts(request, dist):
    fort_data = Forts.objects.filter(fort_district=dist)
    paginator = Paginator(fort_data, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    all_dist = Forts.objects.values_list('fort_district', flat=True).distinct()
    all_districts = set(all_dist)

    return render(request, "knowaboutforts.html", context={"page_obj":page_obj, "all_districts":all_districts})


@login_required(login_url="/login-page/")
def searchfortname(request):
    if request.method == "POST":
        data = request.POST
        fortname = data.get("fortname")

        fort_data = Forts.objects.filter(fort_name__icontains=fortname)
        paginator = Paginator(fort_data, 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        all_dist = Forts.objects.values_list('fort_district', flat=True).distinct()
        all_districts = set(all_dist)

        return render(request, "knowaboutforts.html", context={"page_obj":page_obj, "all_districts":all_districts})


@login_required(login_url="/login-page/")
def viewmore(request, fortname):
    # Need to remove url encoding while getting fort name
    from urllib.parse import unquote
    decoded_fortname = unquote(fortname)
    print('fort name :',fortname)
    
    fort_info = Forts.objects.get(fort_name=decoded_fortname)
    print('fort info:', fort_info)
    fort_link = str(fort_info.link)
    link = request.GET.get('link', fort_link)
    return render(request, "fort_info.html", context={"link":link})

