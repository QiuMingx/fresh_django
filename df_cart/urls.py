from django.conf.urls import url
import views


urlpatterns = [
	url(r'^$', views.cart),
	url(r'^add_(\d+)_(\d+)/$', views.add),
	url(r'^edit_(\d+)_(\d+)/$', views.edit),
	url(r'^delete_(\d+)/$', views.delete),

]