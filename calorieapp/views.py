from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse



def signupuser(request):
    if request.method=="GET":
        return render(request,'calorieapp/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['username']=="" or request.POST['password1']=="":
            return render(request,'calorieapp/signupuser.html',{'error':'Please enter a valid username and password'})
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('caloriecounter')
            except IntegrityError:
                return render(request,'calorieapp/signupuser.html',{'form':UserCreationForm(), 'error':'Username taken! Please choose a new username'})
        else:
            return render(request,'calorieapp/signupuser.html',{'form':UserCreationForm(), 'error':'Password Mismatch!'})

def loginuser(request):
    if request.method=="GET":
        return render(request,'calorieapp/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'calorieapp/loginuser.html',{'form':AuthenticationForm(), 'error':'Username and password do not match'})
        else:
            login(request,user)
            return redirect('caloriecounter')

def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('loginuser')

import csv

path='C:\Django Nick Walter\calorie_counter-project\calories.csv'

with open(path,'r',encoding='utf-8') as file:
    csv_reader=csv.reader(file)
    food_items1 = [row[1] for row in csv_reader]

with open(path,'r',encoding='utf-8') as file:
    csv_reader=csv.reader(file)
    food_items2 = [row[3] for row in csv_reader]

food_items={}

for i in range (len(food_items1)):
    for j in range (len(food_items2)):
        if i==j:
            food_items[food_items1[i]]=food_items2[j]

#print((food_items2))
#print((food_items1))
#print(food_items)





def caloriecounter(request):
    try:
        if request.method=="POST":
            number_of_food_items=int(request.POST.get('number_of_food_items'))
            print(len(food_items))
            url="caltracker/?output={}".format(number_of_food_items)
            return HttpResponseRedirect(url)
        
    except:
        pass
    return render(request,"calorieapp/caloriecounter.html")




def caltracker(request):
    if request.method == "GET":
        number_of_food_items=request.GET.get('output')
    return render(request,'calorieapp/caltracker.html', {'number_of_food_items': number_of_food_items,'food_items':food_items})
    


def showcalorie(request):
    quan=0
    number_of_food_items=int(request.POST.get("readonlyField"))
    food_entries=[]
    total_calories=0
    error=""
    nofood=[]
    for i in range(number_of_food_items):
        food_item = request.POST.get(f'food_item_{i+1}')
        food_item = food_item.title()
        quantity1 = request.POST.get(f'quantity_food_item_{i+1}')
        quan=int(quantity1)

        if food_item.casefold() in [item.casefold() for item in food_items]:
            try:
                calories = int(food_items[food_item].split()[0])*(quan/100)
                total_calories += calories
                food_entries.append({'food_item': food_item, 'calories': calories, 'quantity':quan})
            except KeyError:
                calories=0
                total_calories=0
                if error!="":
                    error=error+", "+food_item
                else:
                    error+=food_item
                error=error+" - currently unavailable. Sorry for the inconvenience!"

        else:
            total_calories+=0
            nofood.append(food_item)
            if error!="":
                error=error+", "+food_item
            else:
                error+=food_item
    
    if error!="" and len(nofood)==1:
        error=error+" is currently unavailable. Sorry for the inconvenience!"
    elif error!="" and len(nofood)>1:
        error=error+" are currently unavailable. Sorry for the inconvenience!"

    total_calories = "{:.2f}".format(total_calories)

    return render(request,"calorieapp/showcalorie.html",{'food_entries':food_entries,'number_of_food_items':number_of_food_items, 'total_calories':total_calories,'error':error})


