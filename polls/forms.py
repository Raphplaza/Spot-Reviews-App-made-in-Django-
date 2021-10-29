from django import forms

class NewSpotForm(forms.Form):
    new_spot = forms.CharField(label='Spot name:', max_length=100)
    #new_spot_country = forms.CharField(label='Country', max_length=100)

class NewSpotReviewForm(forms.Form):
    new_spot_review = forms.CharField(label='Write your review:', max_length=100)
    author_name = forms.CharField(label='author name:', max_length=30)