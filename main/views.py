from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .authentication import SignUp, Login
from .forms import UserCreadential_Form as creadential_form, UserProfile_Form, LoginForm, UrlForm, Search

from bs4 import BeautifulSoup
import requests
from .scrape import Request_Data, Soup, Filter_soup

# Create your views here.

def index(request):
    forms = {
        'credentialForm' : creadential_form,
        'userProfileForm' : UserProfile_Form,
        'loginForm' : LoginForm,
        'warning' : ''
    }

    if 'id' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password =  request.POST['password']
        signup_form = creadential_form(request.POST)
        login_form = LoginForm(request.POST)
        profile_form = UserProfile_Form(request.POST)

        if signup_form.is_valid() and profile_form.is_valid(): #for signUp
            signup = SignUp(
                email,
                password,
                request.POST['first_name'],
                request.POST['last_name']
            )

            if not signup.email_exist():
                signup.register_user()
                request.session['id'] = signup.get_account(id=True)
                return redirect('home')
            else:
                forms['warning'] = 'Email Already Exist'

        elif login_form.is_valid(): #for signIn
            login = Login(email, password, request)

            if login.verified():
                request.session['id'] = login.verified()
                return redirect('home')
            else:
                forms['warning'] = 'Invalid Email or Password'
        
            
    return render(request, 'main/index.html', forms)



def home(request):
    data = {
        'id' : request.session['id'],
        'input' : UrlForm(),
        'search_input' : Search(),
        'no_filter' : '',
        'filter_tag' : ''
    }

    if request.method == 'POST':
        url_input = UrlForm(request.POST)
        search_input = Search(request.POST)

        if url_input.is_valid():
            #check if the session['link'] not exist or not equal to url on input html to prevent multiple request on the same website
            if 'link' not in request.session or request.session['link'] != request.POST['url'] and 'https:' in request.session['link'] or 'http:' in request.session['link']:
                lxml = Request_Data(request.POST['url'], request)
                request.session['html'] = lxml.html

            request.session['link'] = request.POST['url']
            request.session['tag'] = request.POST['tags']
            request.session['type'] = request.POST['type']
            request.session['name'] = request.POST['search']
            request.session['get_text'] = request.POST['get']


    if 'link' in request.session:
        data['link'] = request.session['link']
        data['tag'] = request.session['tag']

        if 'html' in request.session:
            tag = request.session['tag']
            type_ = request.session['type']
            name = request.session['name']
            get_text = request.session['get_text']

            #filtering the data using the tag, type, name, and get_text
            soup = Soup(request.session['html'], 'lxml')
            datas = soup.get(tag, type_, name, get_text)

            #check if the tag is none if not none it will not change the data['table_head]
            data['table_head'] = f'<{tag} {type_}="{name}"'
            if type_ == 'none':
                data['table_head'] = f'<{tag}'



            if request.method == 'POST':
                if 'filter-get' in request.POST:
                    filter_get = request.POST['filter-get']
                    if filter_get != 'filter-tag':
                        if filter_get == 'text':
                            datas = Filter_soup(datas).filter_get()
                        else:
                            datas = Filter_soup(datas).filter_attribute(filter_get)

                    else:
                        if 'filter-tag-input'  in request.POST and request.POST['filter-find-by'] == 'filter-none':
                            datas = Filter_soup(datas).filter_tag_NoClassAndID(request.POST['filter-tag-input'])
                        else:
                            datas = Filter_soup(datas).filter_tag_wClassOrID(
                                request.POST['filter-tag-input'],
                                request.POST['filter-find-by'],
                                request.POST['filter-find-by-input']
                            )

                        data['filter_tag'] = request.POST['filter-tag-input']
                        data['filter_tag_by'] = request.POST['filter-find-by']
                        data['filter_by_input_value'] = request.POST['filter-find-by-input']

                    get_text = filter_get
                    data['no_filter'] = filter_get

                    print(len(datas))
                    
            #convert the data to string to display all
            temp_datas = []
            for dat in datas:
                temp_datas.append(str(dat))
            
            if len(temp_datas) == 0:
                temp_datas = ['No Item']
            

            #addting dictionary from data to render on the page
            data['data'] = {
                'datas' : temp_datas,
                'length' : len(temp_datas),
                'selection': str(get_text).upper()
            }
 

    return render(request, 'main/home.html', data, status=200)


def logout(request):
    del request.session['id']
    if 'link' in request.session:
        del request.session['link']
    return redirect('index')