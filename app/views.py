from django.shortcuts import render,redirect
from .forms import *
from .models import *
import math
from django.http import HttpResponse
from greenfresh.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from django.contrib import messages

import razorpay
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Create your views here.
def index(request):
	
	if request.method=="POST":
		print(33333333)
		form=SigninForm(request.POST)
		if form.is_valid():
			cust=Customer.objects.filter(email=form.cleaned_data['mail']).first()

			if cust!= None and cust.password== form.cleaned_data['password']:
				request.session['cust']=cust.email
				print(request.session['cust'])
				return redirect('home')
			else:
				return HttpResponse('wrong credintials')
		else:
			form=SigninForm()
			return render(request,'login.html',{'form':form,'type':'signin'})

	else:
		form=SigninForm()
		return render(request,'login.html',{'form':form,'type':'signin'})

def signup(request):
	print(request)
	if request.method=="POST":
		form=SignupForm(request.POST)
		print(11111)
		
		if form.is_valid():
			print(22222)
			cust=Customer()
			(cust.name,cust.password,cust.email)=(request.POST.get('your_name'),request.POST.get('password'),request.POST.get('Email'))
			cust.save()
			return redirect('signin')
		
		else:
			return HttpResponse('form is invlid') 
		
	else:
		form=SignupForm()
		return render(request,'login.html',{'form':form,'type':'signup'})

def home(request):
	veggi=Product.objects.all()
	print(veggi)
	all_cate=[i.cate for i in veggi]
	print(all_cate) 
	cate=set()
	for v in veggi:
		cate.add(v.cate)
	slides=dict()
	for c in cate:
		count=all_cate.count(c)
		slides[str(c)]={'1':math.floor(count/3),'2':[i for i in veggi if i.cate==c]}
	print(slides)
	if 'cust' in request.session.keys():
		cus=request.session['cust']
	else:
		cus=False
	print(cus)
	return render(request,'home.html',{'cate':cate,'slides':slides,'veggi':veggi,'cus':cus})

def cart(request):
	
	if 'cust' in request.session.keys():
	    if request.GET.get('do')=='remove':
	        veggi=Product.objects.filter(name=request.GET.get('veggi')).first()
	        man=Customer.objects.filter(email=request.session['cust']).first()
	        c=Cart.objects.filter(cusid=man,prod=veggi).first()
	        if c.qty== 1:
	            c.delete()
	        else:
	            c.qty-=1
	            c.save()
	        return HttpResponse('removed')
	    
	    elif request.GET.get('do')=='add':
	        
    		print('i got data here')
    		veggi=Product.objects.filter(name=request.GET.get('veggi')).first()
    		print(veggi)
    		man=Customer.objects.filter(email=request.session['cust']).first()
    		print(man)
    		c=Cart.objects.filter(cusid=man,prod=veggi).first()
    		print(c)
    		if c== None:
    			c=Cart()
    			(c.prod,c.cusid,c.qty)=(veggi,man,1)
    			c.save()
    		else:
    			c.qty+=1
    			c.save()
    		return HttpResponse('got data')
	else:
	    return HttpResponse('got no data')
		
		
def gotocart(request):
	if 'cust' in request.session.keys():
		c=Customer.objects.filter(email=request.session['cust']).first()
		data=Cart.objects.filter(cusid=c)
		return render(request,'cart.html',{'data':data,'cus':request.session['cust']})
	else:
		return redirect('signin')
	
	
		
def logout(request):
	if 'cust' in request.session.keys():
		del request.session['cust']
	return redirect('signin')


def contactus(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Your Response is reported')
            return redirect('home')
        else:
            return HttpResponse('form is invlid') 
    form=ContactForm()
    if 'cust' in request.session.keys():
        cus=request.session['cust']
    else:
        cus=False
    return render(request,'login.html',{'form':form,'cus':cus,'type':'contactus'})

def order(request):
    if 'cust' in request.session.keys():
        if  'Street' in request.POST:
            form=AdressForm(request.POST)
            if form.is_valid():
	            add=Adress()
	            (add.street,add.room_no,add.pincode,add.cusid)=(request.POST.get('Street'),request.POST.get('Room_no'),request.POST.get('Pin_code'),Customer.objects.filter(email=request.session['cust']).first())
	            add.save()
	            print(1234)
	            request.session['adress']=add.id
	            return redirect('payment')
        elif 'selected' in request.POST:
            add=Adress.objects.filter(cusid=Customer.objects.filter(email=request.session['cust']).first(),id=int(request.POST.get('selected'))).first()
            request.session['adress']=add.id
            print(request.session['adress'])
            return redirect('payment')
        else:
            c=Customer.objects.filter(email=request.session['cust']).first()
            adress=Adress.objects.filter(cusid=c)
            data=Cart.objects.filter(cusid=c)
            form=AdressForm()
            return render(request,'order.html',{'data':data,'cus':request.session['cust'],'adress':adress,'falg':False,'form':form})

            
    else:
        return redirect('signin')
        
        
def payment(request):
    if request.method== 'POST':
        order=Order()
        order.id=request.POST.get('payment_id')
        order.adress=Adress.objects.filter(id=request.session['adress']).first()
        order.save()
        
        for itom in Cart.objects.filter(cusid=Customer.objects.filter(email=request.session['cust']).first()):
            #add same itom to orderd products
            pro_ord=Prod_orderd()
            pro_ord.order_id=order
            pro_ord.prod=itom.prod
            pro_ord.qty=itom.qty
            pro_ord.save()
            #romove same product from Cart
            itom.delete()
            
        return redirect('home')
    else:
        c=Customer.objects.filter(email=request.session['cust']).first()
        adress=Adress.objects.filter(cusid=Customer.objects.filter(email=request.session['cust']).first())
        data=Cart.objects.filter(cusid=c)
        form=AdressForm() 
        sum=0;
                
        for row in data :
            sum=sum + row.total
            print(sum)
                #order amount in paisa so amount*100 Rs
        order_amount = sum*100
        order_currency = 'INR'
                
                #object of client order
        payment_order = client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1))
        payment_order_id =payment_order['id']
                
               
        context ={
                    'amount':sum,
                    'name':c.name,
                    'email':c.email,
                    'order_id' : payment_order_id,
                    'key' : RAZORPAY_KEY_ID,
                    'data':data,'cus':request.session['cust'],'adress':adress,'form':form,'flag':True
                }
            
        return render(request,'order.html',context)
    
    
    
	# if 'cust' in request.session.keys():
	    # if request.method=='POST':
	        # form=AdressForm(request.POST)
	        # if form.is_valid():
	            # add=Adress()
	            # (add.street,add.room_no,add.pincode,add.cusid)=(request.POST.get('Street'),request.POST.get('Room_no'),request.POST.get('Pin_code'),Customer.objects.filter(email=request.session['cust']).first())
	            # add.save()
	            # return HttpResponse('done')
	    # else:
    		# c=Customer.objects.filter(email=request.session['cust']).first()
    		# adress=Adress.objects.filter(cusid=c)
    		# data=Cart.objects.filter(cusid=c)
    		# form=AdressForm()
    		# return render(request,'order.html',{'data':data,'cus':request.session['cust'],'adress':adress,'form':form})
	# else:
		# return redirect('signin')
	