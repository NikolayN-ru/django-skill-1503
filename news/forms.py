from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['author', 'choice', 'category', 'title', 'content']
		# fields = '__all__'
		widgets = {
			'author': forms.Select(attrs={'class': 'form-control'}),
			'choice': forms.Select(attrs={'class': 'form-control'}),
			'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
		}

class PostForm2(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)

class PersonForm(forms.Form):
	first_name = forms.CharField()

class ContactFormPWithPriority(ContactForm, PersonForm):
	priority = forms.CharField()
	cc_myself = None
	# prefix = 'person'



