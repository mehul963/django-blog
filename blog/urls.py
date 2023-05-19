from django.urls import path
from . import views
handler404 = 'blog.views.custom_404'

urlpatterns = [
    path("",views.home,name='home'),
    path("blog/<slug:blog_id>",views.show,name='blog'),
    path("login",views.login,name='login'),
    path("signup",views.signup,name='signup'),
    path("write",views.write_blog,name='write blog'),
    path("verify/<str:token>",views.verify,name='write blog'),
    path("forget",views.forget_password,name='forget password'),
    path("search",views.search,name='search'),
    path("logout",views.logout,name='logout'),
] 

htmx_urls=[
    path("post",views.save_artical),
    path("reset/<str:token>",views.reset),
]

urlpatterns+=htmx_urls