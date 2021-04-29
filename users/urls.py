from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
    url('^login/$', 'login', name='login'),
    url('^logout/$', 'logout', name='logout'),
    url(r'^find-friends/$', 'find_friends', name='find_friends'),
    url(r'^modify-friend/$', 'modify_friend', name='modify_friend'),
)