"""Определяет схемы URL для learning_logs """

from django.conf.urls import url

from . import views

urlpatterns = [
    # Домашняя стр
    url(r'^$', views.index, name='index'),
    # Вывод тем
    url(r'^topics/$', views.topics, name='topics'),
    # Страница с подбробной информацией по отдельной теме
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    url(r'^new_topics/$', views.new_topics, name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

]