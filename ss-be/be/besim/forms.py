from django import forms

class NameForm(forms.Form):
    CHOICES=[('1','Scenario 1'),('2','Scenario 2')]
    card_number = forms.CharField(label='Card Number', max_length=100)
    use_cases = forms.ChoiceField(label='Scenarios', choices=CHOICES,widget=forms.RadioSelect())
    class Media:
         css = {
             'all': ('/static/besim/css/besim.css',),
         }
         js = ('/static/besim/js/jquery.js', '/static/besim/js/besim.js')


class UsecaseForm(forms.Form):
    amount =  forms.CharField(label='My bill is...', max_length=100)
    class Media:
         css = {
             'all': ('/static/besim/css/besim.css')
         }
         js = ('/static/besim/js/besim.js')


