from django import forms

import re


lsentity = (
    ('',          ''),
    ('word',      'word'),
    ('sentence',  'sentence'),
    ('paragraph', 'paragraph'),
    ('text',      'text'),
)


class ImageDemoForm(forms.Form):
    width = forms.IntegerField(required=False, min_value=1, max_value=2000, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}), label='Image width', help_text='In pixels ( default: 640 )')
    height = forms.IntegerField(required=False, min_value=1, max_value=2000, label='Image height', help_text='In pixels ( default : 480 )')
    front = forms.CharField(required=False, max_length=16, widget=forms.TextInput(attrs={'list': 'color'}), label='Text color', help_text='Color name or hexadecimal color code ( default : #666 )')
    back = forms.CharField(required=False, max_length=16, widget=forms.TextInput(attrs={'list': 'color'}), label='Background color', help_text='Color name or hexadecimal color code ( default : #999 )')
    text = forms.CharField(required=False, max_length=64, label='Text on image', help_text='May contain %(...)s formatting conversion specifiers ( default : %(width)s x %(height)s )')


    def clean_front(self):
        data = self.cleaned_data['front']
        if data and not re.match(r'[a-z]+$', data, re.I) and not re.match(r'#([0-9a-f]{3}){1,2}$', data, re.I):
            raise forms.ValidationError('Enter color name or hexadecimal color code')

        return data


    def clean_back(self):
        data = self.cleaned_data['back']
        if data and not re.match(r'[a-z]+$', data, re.I) and not re.match(r'#([0-9a-f]{3}){1,2}$', data, re.I):
            raise forms.ValidationError('Enter color name or hexadecimal color code')

        return data


class TextDemoForm(forms.Form):
    entity = forms.ChoiceField(required=False, choices=lsentity, widget=forms.Select(attrs={'autofocus': 'autofocus'}), label='Entity to generate', help_text='Unit of measurment ( default : text )')
    length = forms.IntegerField(required=False, min_value=1, max_value=100, label='Entity length', help_text='Number of contained subitems ( default : 5 for text, random for others )')
    sample = forms.CharField(required=False, widget=forms.Textarea, label='Sample text', help_text='Text to analyze ( default : <a href="http://python.org/dev/peps/pep-0020/">The Zen of Python</a> )')
