from django import template

register = template.Library()

@register.filter(name='times')
def times(dic):
	
	dic=dict(dic)
	number=dic['1']
	
	return range(int(number))

@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None

@register.filter
def trim(lst,loopval):
    try:
    	
    	cut=3*loopval
    	
    	return lst[cut:]
    except:
        return None

@register.filter(name='lambi')
def lambi(dic):
	dic=dict(dic)
	lis=dic['2']
	
	return len(lis)

@register.filter(name='rang')
def rang(dic):
	dic=dict(dic)
	lis=dic['2']
	return range(len(lis))