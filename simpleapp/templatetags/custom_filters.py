from django import template
import re

register = template.Library()

# {% load custom_filters %}

@register.filter(name='multiply')
def multiply(value, arg):
	if isinstance(value, str) and isinstance(arg, int):
		return str(value) * arg
	else:
		raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
	return str(value) * arg

@register.filter(name='Censor')
def Censor(value):
	if isinstance(value, str):
		a = ['ху', 'пизд', 'нах', 'жоп', 'ебл', 'бля']
		for i in a:
			value = re.sub(f'{i}', '♥♥', value)
	return value