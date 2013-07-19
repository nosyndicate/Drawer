'''
Created on 2013-7-15

@author: nosyndicate
'''
from django import forms
from models import Summary, Author

class SummaryCreateForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}))
    authors = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}));
    media = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);
    areas = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);
    keywords = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);
    summary = forms.CharField(widget=forms.Textarea(attrs={"class":"blockinput"}))
    questions = forms.CharField(widget=forms.Textarea(attrs={"class":"blockinput"}),required=False)

    def is_valid(self):
        return True


class SummaryBaseInfoForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}))
    authors = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}));
    media = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);
    areas = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);
    keywords = forms.CharField(widget=forms.TextInput(attrs={"class":"lineinput"}),required=False);


class EditionForm(forms.Form):
    summary = forms.CharField(widget=forms.Textarea(attrs={"class":"blockinput"}))
    questions = forms.CharField(widget=forms.Textarea(attrs={"class":"blockinput"}),required=False)
