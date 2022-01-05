from django.contrib.auth.models import User
from django.shortcuts import render, redirect #untuk memanggil file html
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.db import transaction
from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse #format html langsung ditulis didalam HttpResponse
from blog.models import Artikel, Kategori
#from demo.mysite.blog.models import Kategori
from users.models import Biodata

def index(request):
    template_name = 'front/index.html'
    artikel = Artikel.objects.all()
    kategori = Kategori.objects.all()
    
    page = request.GET.get('page', 1)

    paginator = Paginator(artikel, 3)
    try:
        artikel = paginator.page(page)
    except PageNotAnInteger:
        artikel = paginator.page(1)
    except EmptyPage:
        artikel = paginator.page(paginator.num_pages)
    context = {
        'title':'my home',
        'artikel': artikel,
         'kategori':kategori,
    }
    return render(request, template_name, context)

def artikel_filter(request, nama):
    template_name = 'front/index.html'
    kategori = Kategori.objects.all()
    artikel = Artikel.objects.filter(kategory__nama=nama)
    context = {
        'title':'my home',
        'artikel': artikel,
         'kategori':kategori,
    }
    return render(request, template_name, context)


def detail_artikel(request, id):
    template_name = 'front/detail_artikel.html'
    artikel = Artikel.objects.get(id=id)
    context = {
        'title':'detail',
        'artikel':artikel
    }
    return render(request, template_name, context)


def about(request):
    template_name = 'front/about.html'
    #data = Biodata.objects.all()
    #print(data)
    context = {
        'title':'about',
        'welcome':'ini page about',
        #'data': data,
    }
    # return HttpResponse('<h1> my home</h1>') #pilih apakah ingin menggunakan Httpresponse atau render
    return render(request, template_name, context)

def login(request):
    if request.user.is_authenticated:
        print('sudah login')
        return redirect('index')
    template_name = "account/login.html"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            #data ada
            print('username benar')
            auth_login(request, user)
            return redirect('index')
            
        else:
            #data tidak ada
            print('username salah')
    context = {
        'title':'form login'
    }
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('index')

def registrasi(request):
    template_name = "account/register.html"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        telp = request.POST.get('telp')
        try:
            with transaction.atomic():
                User.objects.create(
                    username = username,
                    password = make_password(password),
                    first_name = nama_depan,
                    last_name = nama_belakang,
                    email = email,
                )
                get_user = User.objects.get(username = username)
                Biodata.objects.create(
                    user = get_user,
                    alamat = alamat,
                    telp = telp,
                )
            return redirect(index)
        except:pass
            #pass
    context = {
        'title':'form registrasi'
    }
    return render(request, template_name, context)
