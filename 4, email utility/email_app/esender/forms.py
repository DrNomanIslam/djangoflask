from django import forms

class EmailForm(forms.Form):
	frm = forms.EmailField(label='From', max_length=100)
	to = forms.EmailField(label='To', max_length=100)
	cc = forms.CharField(label='CC', max_length=100, required=False)
	subject = forms.CharField(label='Subject', max_length=100)
	message = forms.CharField(label='Message', max_length=1000)
	
    