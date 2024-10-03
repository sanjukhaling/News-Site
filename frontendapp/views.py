from django.shortcuts import render,redirect

# Create your views here.
from audioop import reverse
from multiprocessing import context
from unicodedata import category, name
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from backendapp.forms import *
from mainapp.models import *
from datetime import datetime



class HomeView(TemplateView):
    template_name = "clienttemplates/basehome/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entertainment = News.objects.filter(category__slug="entertainment").order_by('-id')[:3]
        sportnews = News.objects.filter(category__slug="sports").order_by('-id')[:5]
        health = News.objects.all().order_by('id')[:5]
        politics = News.objects.all().order_by('id')[:5]
        banners = News.objects.all().order_by('id')[:7]
        slider = News.objects.all().order_by('-id')[:7]
        features = News.objects.all().order_by('id')[:8]
        business = News.objects.filter(category__slug="business").order_by('-id')[:5]
        technology = News.objects.filter(category__slug="technology").order_by('-id')[:5]

        # politic = News.objects.filter(category__slug="politics").order_by('-id')[:5]

        populars = News.objects.all().order_by('-id')[:1]
        populars2 = News.objects.all().order_by('-id')[1:2]
        populars3 = News.objects.all().order_by('id')[3:5]
        populars4 = News.objects.all().order_by('id')[5:7]

        latest = News.objects.all().order_by('-id')[:1]
        latest2 = News.objects.all().order_by('-id')[1:2]
        latest3 = News.objects.all().order_by('id')[3:5]
        latest4 = News.objects.all().order_by('id')[5:7]
        newscat = NewsCategory.objects.all().order_by('-id')[:4]
        tranding = News.objects.all().order_by('id')[5:12]

        ####Ads####
        ads = Ads.objects.all()
        ads1 = Ads.objects.all()
        ads2 = Ads.objects.all()

        context['ads_1'] = ads
        context['ads_2'] = ads1
        context['ads_3'] = ads2

        context["entnews"] = entertainment
        context["sports"] = sportnews
        context["health"] = health
        context["politic"] = politics
        context["banners"] = banners
        context["slider"] = slider
        context["features"] = features
        context["busi"] = business
        context["techno"] = technology
        context['popularnews'] = populars
        context["popularnews2"] = populars2
        context['populars3'] = populars3
        context["populars4"] = populars4

        context["latest"] = politics

        context["latest"] = latest
        context["latest2"] = latest2
        context["latest3"] = latest3
        context["latest4"] = latest4

        context["categories"] = newscat
        context["tranding"] = tranding

        return context


class NewsDetailView(CreateView):
    template_name = "clienttemplates/news/newsdetail.html"
    form_class = NewsCommentForm

    # success_url = reverse_lazy("myapp:home")

    def get_success_url(self, **kwargs):
        return reverse_lazy("frontendapp:newsdetail", kwargs={'id': self.request.POST.get("news")})

    # for view count
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # taking news id
        news_id = self.kwargs['id']
        # geting object from News model(using id filter)
        obj = News.objects.get(id=news_id)
        # view count increment by 1 (in view_count field)
        obj.view_count += 1
        # saving data on database(i.e. News model)
        obj.save()

        trending_object = News.objects.all().order_by('-view_count')[:5]
        context["trendings"] = trending_object
        # news object
        context["dnews"] = News.objects.get(id=news_id)

        context["comments"] = NewsComment.objects.filter(news=news_id).order_by('-id')

        newscat = NewsCategory.objects.all().order_by('id')[:4]
        context['categories'] = newscat



        return context


class NewsCategoryListView(TemplateView):
    template_name = "clienttemplates/newscategory/newscategory.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = self.kwargs['slug']
        categorynews = News.objects.filter(category__slug=cat)[:4]
        # breakpoint()
        context["catnews"] = categorynews

        newscat = NewsCategory.objects.all().order_by('id')[:4]
        context['categories'] = newscat

        return context


class ContactView(TemplateView):
    template_name = "clienttemplates/contact/contact.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        our_detail = OurContact.objects.first()

        context['contacts'] = our_detail

        context['form'] = ContactForm

        newscat = NewsCategory.objects.all().order_by('id')[:4]
        context['categories'] = newscat

        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact_form.save()
        else:
            return render(request, self.template_name, {'form': contact_form, 'msg_error': 'sorry! invalid'})
        return redirect('backendapp:contact_list')

    #####STAFF######


class StaffListView(TemplateView):
    template_name = 'clienttemplates/staff/stafflist.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)

        staff_list = Staff.objects.all().order_by('id')
        context['staff_list'] = staff_list

        news = News.objects.all().order_by('-id')[:6]
        context['news'] = news

        newscat = NewsCategory.objects.all().order_by('id')[:8]
        context['categories'] = newscat

        return context





