from django.contrib import messages
from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth import authenticate, logout, login
from rest_framework.response import Response


# from .views_api import *

# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs': BlogModel.objects.all()}

    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')


def login_self(request):
    if request.method == "POST":
        response = {}
        response['status'] = 500
        response['message'] = 'something went wrong'

        try:


            # if data.get('username') is None:
            #     response['message'] = 'Key username not found'
            #     raise Exception('key username not found')
            #
            # if data.get('password') is None:
            #     response['message'] = 'Key password not found'
            #     raise Exception('key password not found')

            # check_user = Person(email=request.POST.get('username')).first()
            #
            # if check_user is None:
            #     response['message'] = 'invalid username, key username not found'
            #     raise Exception('invalid User name')
            print(request.POST.get('username'))
            print(request.POST.get('password'))
            user_obj = authenticate(email=request.POST.get('username'), password=request.POST.get('password'))

            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = 'Welcome'
            else:
                response['message'] = 'invalid password'
                error_message = 'invalid password'
                raise Exception('invalid password')
                return render(request, 'login.html', response)

        except Exception as e:
            print(e)
            error_message = 'invalid password'
            return render(request, 'login.html', response)

    return redirect('/add-blog')


def blog_detail(request, slug):
    context = {}

    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs

    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)


def add_blog(request):
    context = {'form': Blogform}

    try:
        if request.method == 'POST':
            form = Blogform(request.POST)
            image = request.FILES['image']
            # request.POST.
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            BlogModel.objects.create(
                user=user, title=title, content=content, image=image
            )
            return redirect('/add-blog')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)
    return render(request,'see_blog.html')

def blog_update(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')
        initial_dict = {'content': blog_obj.content}
        form = Blogform(initial=initial_dict)

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', context)


def register_view(request):
    return render(request, 'register.html')


def registered_data(request):
    if request.method == "POST":
        if request.POST.get('Firstname') and request.POST.get('Lastname') and request.POST.get(
                'email') and request.POST.get('password') and request.POST.get('confirmpassword'):
            saverecord = Person()
            saverecord.FirstName = request.POST.get('Firstname')
            saverecord.LastName = request.POST.get('Lastname')
            saverecord.email = request.POST.get('email')
            saverecord.password = request.POST.get('password')
            saverecord.confirmpassword = request.POST.get('confirmpassword')
            saverecord.save()
            messages.success(request, 'person' + saverecord.FirstName + 'is saved successfully')
            return redirect('/')
        else:
            return render(request, 'login.html')
