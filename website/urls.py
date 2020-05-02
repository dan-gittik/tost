from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('account', views.account, name='account'),
    path('logout', views.logout, name='logout'),
    path('delete-account', views.delete_account, name='delete-account'),
    path('validate-email', views.validate_email, name='validate-email'),
    path('change-password', views.change_password, name='change-password'),
    path('exercises', views.exercises, name='exercises'),
    path('exercises/<exercise>/test', views.exercise_test, name='exercise-test'),
    path('exercises/<exercise>/cr/files/<path:path>', views.exercise_cr_files, name='exercise-cr-files'),
    path('exercises/<exercise>/cr/notes', views.exercise_cr_files, name='exercise-cr-files'),
    path('exercises/<exercise>/forum', views.forum, name='forum'),
    path('exercises/<exercise>/forum/add', views.add_post, name='add-post'),
    path('exercises/<exercise>/forum/<post>', views.post, name='post'),
    path('exercises/<exercise>/forum/<post>/edit', views.edit_post, name='edit-post'),
    path('exercises/<exercise>/forum/<post>/delete', views.delete_post, name='delete-post'),
    path('exercises/<exercise>/forum/<post>/comments/add', views.add_comment, name='add-comment'),
    path('exercises/<exercise>/forum/<post>/comments/<comment>/edit', views.edit_comment, name='edit-comment'),
    path('exercises/<exercise>/forum/<post>/comments/<comment>/delete', views.delete_comment, name='delete-comment'),
    path('extension', views.extension, name='extension'),
    path('', views.index, name='index'),
]
