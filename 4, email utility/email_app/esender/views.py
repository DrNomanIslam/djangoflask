from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import EmailForm
from django.core.mail import send_mail


def index(request):
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			frm = form.cleaned_data['frm']
			to = form.cleaned_data['to']
			cc = form.cleaned_data['cc']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			send_mail(subject, message, frm, [to])
			return render(request,'send.html',{'message':'Email sent','form': form})		
	else:
		form = EmailForm()
		return render(request,'send.html',{'form': form})
    	