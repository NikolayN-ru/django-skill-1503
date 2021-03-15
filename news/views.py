from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, PostForm2, ContactForm, ContactFormPWithPriority, PersonForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.signals import post_save, pre_init, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
	print(kwargs,'****************')
	# print(instance.title)
	# print(instance.category)
	# print(list(instance.category))


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Post
	template_name = 'post_delete.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	success_url = '/news/'
	context_object_name = 'news'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Post
	template_name = 'post_update.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	form_class = PostForm

	def get_obect(self, **kwargs):
		pk = self.kwargs.get('pk')
		return Post.objects.get(pk=pk)



class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	template_name = 'post_create.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	form_class = PostForm
	success_url = reverse_lazy('head')

	# def get_obect(self, **kwargs):
	# 	pk = self.kwargs.get('pk')
	# 	return Post.objects.get(pk=pk)

	def post(self, request, *args, **kwargs):
		category = request.POST['category']
		client_text=request.POST['content']
		print(category, '-номер категории-')
		cat = Category.objects.get(pk=category)
		print(cat.subscribers.all(), 'участники категории')
		users = cat.subscribers.all()
		# print(f'{self.request.POST} -PK')  - содержит номер категории
		# new =request.POST['content']
		# print(new)
		# ids = Post.objects.filter(content=new)
		# print(ids, '445')
		# print(ids.get_absolute_url, '888')

		for user in users:
			print(user.email)
			if user.email:
				print(f'нашли юзера, отправляем ему на емаил. {user.email}')

				# send_mail(
				# 	subject = f'{user.email}',
				# 	message = f'{client_text[:50]} - новая запись - ссылка на статью {}',
				# 	from_email = 'napadaylo89@mail.ru',
				# 	recipient_list = [user.email, ],
				# )
				print('---------------------')
				print(user.email)
				print(client_text[:50])
		return redirect('head')



class ProductList(LoginRequiredMixin, ListView):
	paginate_by = 3
	model = Post
	template_name = 'posts.html'
	context_object_name = 'products'
	queryset = Post.objects.order_by('-id')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['is_not_premium'] = not self.request.user.groups.filter(name = 'authors').exists()
		context['category'] = Category.objects.all()
		# context['categoryid'] = Category.objects.get(id=self.kwargs['category'])
		return context

class CategoryList(ListView):
	model = Post
	template_name = 'posts.html'
	context_object_name = 'products'
	queryset = Post.objects.order_by('-id')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['time_now'] = datetime.utcnow()
		context['value1'] = None
		context['is_not_premium'] = not self.request.user.groups.filter(name = 'authors').exists()
		context['category'] = Category.objects.all()
		# context['categoryid'] = Category.objects.get(id=self.kwargs['category'])
		print(context['is_not_premium'], '--------')
		cat = Category.objects.get(id=self.kwargs['category']) #получаем категорию
		myuser = self.request.user
		q=cat.subscribers.all()
		if myuser in q:
			context['categoryidbed'] = Category.objects.get(id=self.kwargs['category'])
		else:
			context['categoryid'] = Category.objects.get(id=self.kwargs['category'])
		return context

	def get_queryset(self):
		return Post.objects.filter(category=self.kwargs['category'])


class ProductDetail(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'new'
	pk_url_kwarg = 'pkl'


class ProductSearch(ListView):
	# paginate_by = 2
	model = Post
	template_name = 'search_posts.html'
	context_object_name = 'products'
	queryset = Post.objects.order_by('-id')
	form_class = PostForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
		context['form'] = PostForm()
		# for i in context:
		# 	print(i)
		return context




class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('news')

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    else:
    	premium_group.user_set.remove(user)
    return redirect('/news')


@login_required
def subscribe(request, category):
	# getemail = request.user.email
	# print('наш полученный емаил', getemail)

	myuser = request.user
	cat = Category.objects.get(id = category)
	# print('наша категория', dir(cat))
	cat.subscribers.add(myuser)
	return redirect(f'/news/category/{category}')


@login_required
def subscribebed(request, category):
	# getemail = request.user.email
	# print('наш полученный емаил', getemail)
	myuser = request.user
	cat = Category.objects.get(id = category)
	cat.subscribers.remove(myuser)
	cat.save()
	print('fffffffffffffffffff')
	return redirect(f'/news/category/{category}')


class AppointmentView(View):

	def get(self, request, *args, **kwargs):
		return render(request, 'form1.html', {})

	def post(self, request, *args, **kwargs):
		appointment = Appointment(
			date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
			client_name=request.POST['client_name'],
			message=request.POST['message'], 
		)
		# print(appointment.is_bound())
		appointment.save()

		html_content = render_to_string(
			'form_created.html', {'appointment': appointment}
		)

		msg = EmailMultiAlternatives(
			subject=f'{appointment.client_name}',
			body=appointment.message,
			from_email='NapadayloNikolay@yandex.ru',
			to=['napadaylonikolay@gmail.com', ]
		)
		msg.attach_alternative(html_content, 'text/html')

		msg.send()

		# send_mail(
		# 	subject = appointment.client_name,
		# 	message = appointment.message,
		# 	from_email = 'NapadayloNikolay@yandex.ru', # от кого
		# 	recipient_list = ['napadaylonikolay@gmail.com', ], # каму на почту придет это письмо	
		# )

		return redirect('form1')

def get_form(request):
	data = {
		'subject': 'data-hello',
		'message': 'hi theme',
		'sender': 'emailmoy@gmail.com',
		'cc_myself': True,
	}
	form = ContactFormPWithPriority(data, label_suffix='->')
	# print(form.is_valid())
	# print(form.is_bound)
	print(form.changed_data)
	# print(form.fields)
	form.order_fields(['cc_myself',])
	return render(request, 'form2.html', {'form':form,})


# from .forms import form

# def get_form(request):
# 	if request.method == 'POST':
# 		new = form(request.POST)
# 		if new.is_valid():
# 			# df=formss.cleaned_data
# 			new.save()
# 			return render()
# 	else:
# 		formss = form()
# 	return render(request, 'template.html', {'formss': formss})



