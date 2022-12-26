from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import requests
import json

# Create your views here.
headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
api_host = "http://localhost:8000"


def register(request):
    if request.method == 'POST':
        if request.POST['Password'] == request.POST['ConfirmPassword']:
            path = "/register?"\
                   + "user_id=" + str(request.POST['ID'])\
                   + "&password=" + str(request.POST['Password'])\
                   + "&email=" + str(request.POST['Email']).replace('@', '%40')
            url = api_host + path
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                return redirect('login')
    return render(request, 'register_page.html')


def login(request):
    if request.method == 'POST':
        path = "/login?"\
               + "user_id=" + str(request.POST['ID'])\
               + "&password=" + str(request.POST['Password'])
        url = api_host + path
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            token = response.json()['access_token']
            response = render(request, 'complete_page.html')
            response.set_cookie('token', token)
            return response
    return render(request, 'login_page.html')


def complete(request):
    if request.method == 'POST':
        response = render(request, 'login_page.html')
        response.set_cookie('token', '')
        return response
    elif request.method == 'GET':
        path = "/verify?" \
               + "token=" + str(request.COOKIES['token'])
        url = api_host + path
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json()['user']['is_admin']:
            return render(request, 'user_management_page.html')
    return render(request, 'complete_page.html')


def management(request):
    path = "/verify?" \
           + "token=" + str(request.COOKIES['token'])
    url = api_host + path
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json()['user']['is_admin']:
        if request.method == 'POST':
            user_id = request.POST['ID']
            user_active = request.POST['is_active']
            user_admin = request.POST['is_admin']
            path = "/user/change/active?" \
                   + "user_id=" + str(user_id)\
                   + "&is_active=" + str(user_active)
            url = api_host + path
            requests.put(url, headers=headers)
            path = "/user/change/admin?" \
                   + "user_id=" + str(user_id) \
                   + "&is_admin=" + str(user_admin)
            url = api_host + path
            requests.put(url, headers=headers)
        elif request.method == 'GET':
            user_id = request.GET['ID']
            path = "/user/delete?"\
                   + "user_id=" + str(user_id)
            url = api_host + path
            requests.delete(url, headers=headers)
    else:
        return redirect('complete_page')
    return render(request, 'user_management_page.html')
