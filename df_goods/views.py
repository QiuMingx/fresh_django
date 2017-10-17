# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.core.paginator import Paginator
from models import *
from df_cart.models import CartInfo

def index(request):
	typelist = TypeInfo.objects.all()
	type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
	type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
	type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
	type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
	type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
	type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
	type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
	type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
	type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
	type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
	type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
	type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
	context = {'title':'首页','guest_cart':1,
			   'type0': type0,'type01':type01,
			   'type1': type1,'type11':type11,
			   'type2': type2,'type21':type21,
			   'type3': type3,'type31':type31,
			   'type4': type4,'type41':type41,
			   'type5': type5,'type51':type51,
			   }

	return render(request,'df_goods/index.html',context)
def list(request,tid,pindex,sort):
	typeinfo = TypeInfo.objects.get(pk=tid)
	gtop = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')[0:2]
	if sort == '1':
		good_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')
	elif sort == '2':
		good_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gprice')
	elif sort == '3':
		good_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gclick')

	p = Paginator(good_list, 5)
	plist = p.page_range
	glist = p.page(int(pindex))
	context = {'title':typeinfo.ttitle,
			   'guest_cart':1,
			   'glist':glist,
			   'typeinfo':typeinfo,
			   'plist':plist,
			   'tid':tid,
			   'sort':sort,
			   'gtop':gtop,
			   }

	return render(request,'df_goods/list.html',context)

def detail(request,gid):
	gdetail = GoodsInfo.objects.get(pk=gid)
	gtop = GoodsInfo.objects.filter(gtype_id=gdetail.gtype_id).order_by('-id')[0:2]

	gdetail.gclick = gdetail.gclick + 1
	gdetail.save()
	context = {'title':gdetail.gtitle,
			   'guest_cart':1,
			   'gdetail':gdetail,
			   'gtop':gtop,

	}
	respose = render(request,'df_goods/detail.html',context)

	goods_ids = request.COOKIES.get('goods_ids','')
	goods_id = '%d'% int(gid)
	if goods_ids != '':
		hold_goods_ids = goods_ids.split(',')
		if hold_goods_ids.count(goods_id) >= 1:
			hold_goods_ids.remove(goods_id)
		hold_goods_ids.insert(0, goods_id)
		if len(hold_goods_ids) >= 6:
		 	hold_goods_ids.pop()
		goods_ids = ','.join(hold_goods_ids)
	else:
		goods_ids = goods_id

	respose.set_cookie('goods_ids',goods_ids)

	return respose

def cart_count(request):
	user_id = request.session['user_id']
	count = CartInfo.objects.filter(user_id = user_id).count()
	if count:
		return count
	else:
		return 0

from haystack.views import SearchView  
  
class MySeachView(SearchView):  
    def extra_context(self):       #重载extra_context来添加额外的context内容  
        context = super(MySeachView,self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1     
        context['cart_ount'] = cart_count(self.request )  
        return context  
