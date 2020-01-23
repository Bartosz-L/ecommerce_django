from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-form-width-small uk-margin-left'}))
