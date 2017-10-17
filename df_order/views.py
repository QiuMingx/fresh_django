# _*_ coding:utf-8 _*_
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import transaction
from df_user.models import UserInfo
from datetime import datetime
from decimal import Decimal
from df_cart.models import *
from models import *
from df_user import user_check


@ user_check.login
def order(request):
	cart_list = request.GET.getlist('cart_id')
	carts = CartInfo.objects.filter(pk__in=cart_list)
	context = {'title':'购物车',
			   'page_name':1,
			   'carts':carts,
	}
	return render(request,'df_order/place_order.html', context)

@ user_check.login
@transaction.atomic
def order_handle(request):
	tran_point = transaction.savepoint()
	cart_ids_string  = request.POST.get('cart_ids')
	try:
		order = OrderInfo()
		now = datetime.now()
		uid = request.session['user_id']
		order.oid ='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
		order.user_id = uid
		order.odate = now
		order.ototal = Decimal(request.POST.get('ototal'))
		order.save()
		cart_ids = [int(item) for item in cart_ids_string.split(',')]
		for cart_id in cart_ids:
			order_detail = OrderDetail()
			order_detail.order = order
			cart = CartInfo.objects.get(id = cart_id)
			goods = cart.goods
			if goods.gstore >= cart.count:
				goods.gstore = cart.goods.gstore - cart.count
				goods.save()
				order_detail.goods_id = goods.id
				order_detail.price = goods.gprice
				order_detail.count = cart.count
				order_detail.save()
				cart.delete()
			else:
				transaction.savepoint_rollback(tran_point)
				return redirect('/cart/')
		transaction.savepoint_commit(tran_point)
	except Exception as e:
		print('=====================%s'% e)
		transaction.savepoint_rollback(tran_point)
	return redirect('/user/order/')