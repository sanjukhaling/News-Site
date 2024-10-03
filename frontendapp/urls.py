from django.urls import path
from .views import *

app_name = "frontendapp"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("category/", CategoryView.as_view(), name="category"),

    path("staff/", StaffListView.as_view(), name="staff"),  # Define the URL pattern
    path("contact/", ContactView.as_view(), name="contact"),  # Define the URL pattern

    path("detailnews/<int:id>-dnews/", NewsDetailView.as_view(), name="newsdetail"),
    path("categorynews/<slug:slug>-list/",NewsCategoryListView.as_view(), name="newscategory"),
    

]
