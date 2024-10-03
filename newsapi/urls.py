from django.urls import path
from .views import *

urlpatterns = [
    #For Login
    path("login/", LoginAPIView.as_view(), name="loginapi"),
    path('get-access/<int:id>/',GetAccessAPIView.as_view(), name="get_access"),


    # For NewsCategory
    path("newscat/list-api/", NewsCategoryListAPIView.as_view(), name="newscat_list_api"),
    path("newscat/create-api/", NewsCategoryCreateAPIView.as_view(), name="newscat_create_api"),
    path("newscat/<int:id>/update-api/", NewsCategoryUpdateAPIView.as_view(), name="newscat_update_api"), 
    path("newscat/<int:id>/delete-api/", NewsCatDeleteAPIView.as_view(), name="newscat_delete_api"),
    path("newscat/<int:id>/detail-api/", NewsCatDetailAPIView.as_view(), name="newscat_detail_api"),


    # For News
    path("news/list-api/", NewsListAPIView.as_view(), name="newslist_api"),
    path("news/create-api/", NewsCreateAPIView.as_view(), name="news_create_api"),
    path("news/<int:id>/update-api/", NewsUpdateAPIView.as_view(), name="news_update_api"),
    path("news/<int:id>/delete-api/", NewsDeleteAPIView.as_view(), name="news_delete_api"),
    path("news/<int:id>/detail-api/", NewsDetailAPIView.as_view(), name="news_detail_api"),


    # For NewsComments
    path("newscomments/list-api/", NewscommentListAPIView.as_view(), name="newscomment_list_api"),
    path("newscomment/create-api/", NewsCommentCreateAPIView.as_view(), name="newscomment_create_api"), 
    path("newscomment/<int:id>/update-api/", NewsCommentUpdateAPIView.as_view(), name="newscomment_update_api"),
    path("newscomment/<int:id>/delete-api/", NewsCommentsDeleteAPIView.as_view(), name="newscomment_delete_api"),
    path("newscomment/<int:id>/detail-api/", NewsCommentDetailAPIView.as_view(), name="newscomment_detail_api"),


    # For AdsCategory
    path("adscat/list-api/", AdsCatListAPIView.as_view(), name="adscat_list_api"),
    path("adscat/create-api/", AdsCatCreateAPIView.as_view(), name="adscat_create_api"),
    path("adscat/<int:id>/update-api/", AdsCatUpdateAPIView.as_view(), name="adscat_update_api"),  
    path("adscat/<int:id>/delete-api/", AdsCatDeleteAPIView.as_view(), name="adscat_delete_api"),
    path("adscat/<int:id>/detail-api/", AdsCatDetailAPIView.as_view(), name="adscat_detail_api"),


    # For Ads
    path("ads/list-api/", AdsListAPIView.as_view(), name="ads_list_api"),
    path("ads/create-api/", AdsCreateAPIView.as_view(), name="ads_create_api"),
    path("ads/<int:id>/update-api/", AdsUpdateAPIView.as_view(), name="ads_update_api"),
    path("ads/<int:id>/delete-api/", AdsDeleteAPIView.as_view(), name="ads_delete_api"),
    path("ads/<int:id>/detail-api/", AdsDetailAPIView.as_view(), name="ads_detail_api"),


    # For Staff
    path("staff/list-api/", StaffListAPIView.as_view(), name="staff_list_api"),
    path("staff/create-api/", StaffCreateAPIView.as_view(), name="staff_create_api"),
    path("staff/<int:id>/update-api/", StaffUpdateAPIView.as_view(), name="staff_update_api"),
    path("staff/<int:id>/delete-api/", StaffDeleteAPIView.as_view(), name="staff_delete_api"),
    path("staff/<int:id>/detail-api/", StaffDetailAPIView.as_view(), name="staff_detail_api"),

    #For Contact
    path("contact/list-api/", ContactListAPIView.as_view(), name="contact_list_api"),
    path("contact/create-api/", ContactCreateAPIView.as_view(), name="contact_create_api"),
    path("contact/<int:id>/update-api/", ContactUpdateAPIView.as_view(), name="contact_update_api"),
    path("contact/<int:id>/delete-api/", ContactDeleteAPIView.as_view(), name="contact_delete_api"),
    path("contact/<int:id>/detail-api/", ContactDetailAPIView.as_view(), name="contact_detail_api"),
]
