from django.urls import path
from .views import ProductList, ProductDetail, ProductSearch, PostCreate, PostUpdate, PostDelete, CategoryList, subscribe, AppointmentView, get_form, subscribebed
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me

urlpatterns = [
	path('subscribebed/<int:category>/', subscribebed, name='subscribebed'),
	path('form1/', AppointmentView.as_view(), name='form1'),
	path('<int:pk>/edit/', PostUpdate.as_view(), name='update'),
	path('<int:pkl>/', ProductDetail.as_view(), name='post'),
	path('category/<int:category>/', CategoryList.as_view(), name='category'),
	path('create/', PostCreate.as_view(), name='create'),
	path('subscribe/<int:category>/', subscribe, name='subscribe'),

	path('search/', ProductSearch.as_view(), name='search'),
	path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
	path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
	path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
	path('upgrade/', upgrade_me, name = 'upgrade'),
	path('form2/', get_form, name='get_form'),
	path('', ProductList.as_view(), name='head'),



]
