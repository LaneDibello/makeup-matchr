from django import forms

class imgForm(forms.Form):
	name = forms.CharField()
	img_field = forms.ImageField()
