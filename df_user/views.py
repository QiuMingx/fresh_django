# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_check
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator

def register(request):
	context = {'title':'用户注册','page_name':1}
	return render(request,'df_user/register.html',context)
	

def register_handle(request):
	"""用户注册"""
	# 接受用户输入
	post = request.POST
	uname = post.get('user_name')
	upwd = post.get('pwd')
	upwd2 = post.get('cpwd')
	uemail = post.get('email')
	# if ((len(uname) < 5 )or (len(uemail)== 0) or (len(upwd) < 8):
	# 	return redirect('/user/register/')
	# 判断两次密码
	if upwd != upwd2:
		return redirect('/user/register/')

	# 密码加密
	s1 = sha1()
	s1.update(upwd)
	upwd3 = s1.hexdigest()
	# 创建对象
	user = UserInfo()
	user.uname = uname
	user.upwd = upwd3
	user.uemail = uemail
	user.save()
	# 注册成功，转到登陆页面
	return redirect('/user/login/')

def register_exist(request):
	uname = request.GET.get('uname')
	count = UserInfo.objects.filter(uname=uname).count()
	return JsonResponse({'count':count})

def login(request):
	uname = request.COOKIES.get('uname','')
	context = {'title':'用户登陆','page_name':1,'error_name':0, 'error_pwd':0, 'uname':uname}
	return render(request, 'df_user/login.html',context)

def login_handle(request):
	# 接收用户信息
	post = request.POST
	uname = post.get('username')
	upwd = post.get('pwd')
	keep_uname = post.get('keepname', 0)
	# 根据用户名查询对象
	users = UserInfo.objects.filter(uname=uname)
	if len(users) == 1:
		s1= sha1()
		s1.update(upwd)
		if s1.hexdigest()==users[0].upwd:
			url = request.COOKIES.get('url','/')
			print(url)
			red = HttpResponseRedirect(url)
			if keep_uname!=0:
				red.set_cookie('uname',uname)
			else:
				red.set_cookie('uname','',max_age=-1)
			request.session['user_id'] = users[0].id
			request.session['user_name'] = uname
			return red
		else:
			context = {'title':'用户登陆','page_name':1,'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
			return render(request,'df_user/login.html',context)
	else:
		context = {'title':'用户登陆','page_name':1,'error_name':1, 'error_pwd':0, 'uname':uname}
		return render(request,'df_user/login.html',context)

@ user_check.login
def info(request):
	user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
	goods_ids = request.COOKIES.get('goods_ids')
	new_list = []
	if goods_ids != None:
		goods_id_list = goods_ids.split(',')
	
		for goods_id in goods_id_list:
			new_good = GoodsInfo.objects.get(id=goods_id)
			new_list.append(new_good)


	context = { 'title':'用户中心',
				'uname':request.session['user_name'],
				'uemail':user_email,
				'page_name':1,
				'new_list':new_list,
				}
	return render(request,'df_user/user_center_info.html',context)

@ user_check.login	
def order(request,pindex):
	user_id = request.session['user_id']
	orders = OrderInfo.objects.filter(user_id=user_id).order_by('-odate')
	order_list =[]
	for order in orders:
		order_list.append([order.oid,order.orderdetail_set.all()])
	if pindex == '':
		pindex = 1
	p = Paginator(orders, 2)
	plist = p.page_range
	olist = p.page(int(pindex))
	context={'title':'用户中心',
	'page_name':1,
	'orders':orders,
	'order_list':order_list,
	'plist':plist,
	'olist':olist,
	}
	return render(request,'df_user/user_center_order.html',context)

@ user_check.login
def site(request):
	user =  UserInfo.objects.get(id=request.session['user_id'])
	if request.method == 'POST':
		post = request.POST
		user.ushou = post.get('ushou')
		user.uaddress = post.get('uaddress')
		user.uyoubian = post.get('uyoubian')
		user.uphone = post.get('uphone')
		user.save()
	context={'title':'用户中心','user':user,'page_name':1}
	return render(request,'df_user/user_center_site.html',context)

def logout(request):
	request.session.flush()
	return redirect('/')