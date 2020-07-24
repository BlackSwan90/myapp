from django.shortcuts import render
from django.http import HttpResponse #added
# Create your views here.

def about_view(request):
	mycontext = {
		'mytext':'nejaky text',
		'mynumber': 1351,
		'mylist': [151,15,1554,2154,121, 'abc']}
	return render(request,'about.html',mycontext)

def css_page_view(request,*args,**kwargs):
	return render(request, 'css_test.html',{})
