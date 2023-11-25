from django.urls import path
from . import views

urlpatterns = [
    path("hello/",views.say_hello),
    path("hello-cached/",views.say_hello_cached),
    path("tags/",views.querying_generic_realtionships),
    path("create/",views.create_object)
    ]