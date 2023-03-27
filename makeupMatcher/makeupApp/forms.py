from django import forms

class imgForm(forms.Form):
	name = forms.CharField()
	img_field = forms.ImageField()
  
# creating a form
class InputForm(forms.Form):

	priceL = forms.IntegerField(widget = forms.NumberInput
                    (attrs = {'class':'form-control',
			                'placeholder':'Min',
			                'aria-label':'Minimum price point'}),
			     label = "Min",
			     required = False)
	priceM = forms.IntegerField(widget = forms.NumberInput
                    (attrs = {'class':'form-control',
			                'placeholder':'Max',
			                'aria-label':'Maximum price point'}),
			     label = "Max",
			     required = False)
	brandName = forms.CharField(max_length = 200,
			     widget = forms.TextInput
                    (attrs = {'class':'form-control',
			                'placeholder':'Brand',
			                'aria-label':'Enter Brand Name'}),
			    label = "Brand",
			    required = False)