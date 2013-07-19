'''
Created on 2013-7-15

@author: nosyndicate
'''

from django.conf.urls import patterns, url

from paperstack import views

urlpatterns = patterns('',
    url(r"^$", views.IndexView.as_view(), name='index'),
    url(r"search", views.SearchView.as_view(), name="search"),
    url(r"create", views.SummaryCreateView.as_view(), name="create"),
    url(r"browse", views.SummaryBrowseView.as_view(), name="browse"),
    url(r"base", views.BaseInfoEditView.as_view(), name="base"),
    url(r"edition", views.EditionView.as_view(), name="edition"),

)
