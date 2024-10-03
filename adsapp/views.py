from audioop import reverse
from django.contrib.auth import authenticate, login,logout
from backendapp.forms import *
from mainapp.models import *
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.http import Http404
from datetime import datetime
from django.utils import timezone


####Ads Category#######
class AdsCategoryCreateView(TemplateView):
    template_name = 'admintemplates/adscategory/adscategorycreate.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdsCategoryForm

        return context

    def post(self, request, *args, **kwargs):
        adscategory_form = AdsCategoryForm(request.POST,request.FILES)
        if adscategory_form.is_valid():
            adscategory_form.save()
            return redirect('adsapp:ads_category_list')
        else:
            return render(request, self.template_name, {'form': adscategory_form, 'msg_error': 'sorry! invalid'})


class AdsCategoryListView(TemplateView):
    template_name = 'admintemplates/adscategory/adscategorylist.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads_list'] = AdsCategory.objects.all()
        return context


class AdsCategoryUpdateView(TemplateView):
    template_name = "admintemplates/adscategory/adscategorycreate.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('id')
        ads_cat = AdsCategory.objects.get(id=cat_id)
        context['form'] = AdsCategoryForm(instance=ads_cat)

        return context

    def post(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('id')
        ads_cat = AdsCategory.objects.get(id=cat_id)
        ads_cat_form = AdsCategoryForm(request.POST, request.FILES, instance=ads_cat)
        if ads_cat_form.is_valid():
            ads_cat_form.save()
            return redirect('adsapp:ads_category_list')
        else:
            return render(request, self.template_name, {'form': ads_cat_form, 'errors_message': 'sorry!!!Not valid'})


class AdsCategoryDeleteView(TemplateView):
    template_name = "admintemplates/adscategory/adscategorydelete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        adscat_id = self.kwargs.get('id')

        try:
            context['ads_cat_delete'] = AdsCategory.objects.get(id=adscat_id)
        except AdsCategory.DoesNotExist:
            raise Http404("adscategory does not exist")
        return context

    def post(self, request, *args, **kwargs):
        news_id = self.kwargs.get('id')
        try:
            adscat_delete = AdsCategory.objects.get(id=news_id)
            adscat_delete.delete()
            # trek_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("news does not exist")
        return redirect('adsapp:ads_category_list')


class AdsCategoryDetailView(TemplateView):
    template_name = "admintemplates/adscategory/adscategorydetail.html"

    # model = News
    # context_object_name = "admin_detail_news"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ads_cat_id = self.kwargs.get('id')
        ads_cat = AdsCategory.objects.get(id=ads_cat_id)
        context['ads_cat_detail'] = ads_cat

        return context


      ####Ads####
class AdsCreateView(TemplateView):
    template_name = 'admintemplates/ads/adscreate.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdsForm

        return context

    def post(self, request, *args, **kwargs):
        ads_form = AdsForm(request.POST,request.FILES)
        if ads_form.is_valid():
            ads_form.save()
            return redirect('adsapp:ads_list')
        else:
            return render(request, self.template_name, {'form': ads_form, 'msg_error': 'sorry! invalid'})


#Ads List

class AdsListView(TemplateView):
    template_name = 'admintemplates/ads/adslist.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all ads
            ads = Ads.objects.all()

            # Calculate remaining days for each ad
            for ad in ads:
                remaining_days = (ad.end_date - timezone.now().date()).days
                ad.remaining_days = max(remaining_days, 0)  # Ensure positive value
            
            # Update remaining_days in bulk
            Ads.objects.bulk_update(ads, ['remaining_days'])

            # Implement pagination
            paginator = Paginator(ads, 10)  # Show 10 ads per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_ads = paginator.get_page(page_number)  # Get paginated results

            # Add paginated ads to the context
            context['ads_list'] = paginated_ads

        except Exception as e:
            messages.error(self.request, "Error fetching ads list.")
            context['ads_list'] = []  # Fallback to an empty list on error

        return context


class AdsUpdateView(TemplateView):
    template_name = "admintemplates/ads/adscreate.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('id')
        ads = Ads.objects.get(id=cat_id)
        context['form'] = AdsForm(instance=ads)

        return context

    def post(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('id')
        ads_cat = Ads.objects.get(id=cat_id)
        ads_form = AdsForm(request.POST, request.FILES, instance=ads_cat)
        if ads_form.is_valid():
            ads_form.save()
            return redirect('adsapp:ads_list')
        else:
            return render(request, self.template_name, {'form': ads_form, 'errors_message': 'sorry!!!Not valid'})


class AdsDeleteView(TemplateView):
    template_name = "admintemplates/ads/adsdelete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ads_id = self.kwargs.get('id')
        try:
            context['ads_delete'] = Ads.objects.get(id=ads_id)
        except Ads.DoesNotExist:
            raise Http404("ads does not exist")
        return context

    def post(self, request, *args, **kwargs):
        ads_id = self.kwargs.get('id')
        try:
            ads_delete = Ads.objects.get(id=ads_id)
            ads_delete.delete()
            # trek_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("ads does not exist")
        return redirect('adsapp:ads_list')


class AdsdetailView(TemplateView):
    template_name = "admintemplates/ads/adsdetail.html"

    # model = News
    # context_object_name = "admin_detail_news"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ads_id = self.kwargs.get('id')
        ads = Ads.objects.get(id=ads_id)
        context['ads_detail'] = ads

        return context
