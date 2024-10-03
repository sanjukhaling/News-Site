from django.urls import path
from .views import *

app_name = "adsapp"

urlpatterns = [
    ####Ads Category####
    path('adscat/', AdsCategoryCreateView.as_view(), name="ads_category_create"),
    path('adscat/list', AdsCategoryListView.as_view(), name="ads_category_list"),
    path('adscat/<int:id>update', AdsCategoryUpdateView.as_view(), name="ads_category_update"),
    path('adscat/<int:id>detail', AdsCategoryDetailView.as_view(), name="ads_category_detail"),
    path('adscat/<int:id>delete', AdsCategoryDeleteView.as_view(), name="ads_category_delete"),

    ####Ads###
    path('ads/create', AdsCreateView.as_view(), name="ads_create"),
    path('ads/list', AdsListView.as_view(), name="ads_list"),
    path('ads/<int:id>update', AdsUpdateView.as_view(), name="ads_update"),
    path('ads/<int:id>detail', AdsdetailView.as_view(), name="ads_detail"),
    path('ads/<int:id>delete', AdsDeleteView.as_view(), name="ads_delete"),
]
