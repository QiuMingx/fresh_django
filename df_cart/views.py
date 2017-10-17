# _*_ coding:utf-8 _*_
from django.shortcuts import render,redirect
from models import *
from df_user import user_check
from django.http import JsonResponse

@ user_check.login
def cart(request):
	user_id = request.session['user_id']
	carts = CartInfo.objects.filter(user_id=user_id)

	context = { 'title':'购物车',
				'page_name':1,
				'carts':carts,
	}
	if request.is_ajax():
		count = CartInfo.objects.filter(user_id=user_id).count()
		return JsonResponse({'count':count})
	return render(request, 'df_cart/cart.html',context)

@ user_check.login
def add(request, gid, num):
	user_id = request.session['user_id']
	carts = CartInfo.objects.filter(goods_id=gid, user_id=user_id)
	if len(carts) > 0:
		cart = carts[0]
		cart.count = cart.count + 1
	else:
		cart = CartInfo()
		cart.goods_id = gid
		cart.user_id = user_id
		cart.count = num
	cart.save()

	if request.is_ajax():
		count = CartInfo.objects.filter(user_id=user_id).count()
		return JsonResponse({'count':count})
	else:
		return redirect('/cart/')
	

@ user_check.login
def edit(request, cid, num):
	try:
		cart = CartInfo.objects.get(pk=cid)
		cart_num = cart.count
		cart.count = num
		cart.save()
		data = {'ack': 'ok'}
	except Exception as e:
		data = {'ack': cart_num }
	return JsonResponse(data)



@ user_check.login
def delete(request, cid):
	try:
		cart = CartInfo.objects.get(pk=cid)
		cart.delete()
		data = {'ack': 1}
	except Exception as e:
		data = {'ack': 0 }
	return JsonResponse(data)

