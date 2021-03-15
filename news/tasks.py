import datetime
from .models import Post
from django.core.mail import send_mail

def send_mails():
	print('Hello_form_backgroud_task')
	now = datetime.datetime.now()
	then = datetime.datetime(2021, 1, 1)
	delta = now - then
	now2 = now.month - 1
	print(now2)
	q = Post.objects.filter(date=f'2021,{now2},{now.day}')
	print(q)
	if delta / 7 == 0:
		print('дни кратны семи')
		print('вычитаем семь дней', delta - 7)
		send_mail(
			subject = 'last month',
			message = q,
			from_email = 'NapadayloNikolay@yandex.ru', # от кого
			recipient_list = [request.user.email, ], # каму на почту придет это письмо	
		)
		# Post.objects.filter(date=)
	else:
		print('некратны')
