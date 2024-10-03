from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True



GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other'),
)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

#NewsCategory
class NewsCategory(DateTimeModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=400, blank=True, null=True)
    # image = models.CharField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to="newscategory/", null=True, blank=True)

    def __str__(self):
        return self.title


class News(DateTimeModel):
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, null=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="News/", null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    banner = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class NewsComment(DateTimeModel):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


SELERSTATUS = (
    ('Accepted', 'Accepted'),
    ('Pending', 'Pending'),
)


class OurContact(DateTimeModel):
    title = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Changed to CharField for flexibility
    maps = models.URLField(max_length=200, blank=True, null=True)


class Contact(DateTimeModel):
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AdsCategory(DateTimeModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title


class Ads(DateTimeModel):
    title = models.CharField(max_length=50)
    issue_date = models.DateField()
    end_date = models.DateField()
    image = models.CharField(max_length=400, blank=True, null=True)
    sponsorships = models.CharField(max_length=20)
    remaining_days = models.PositiveIntegerField(blank=True, null=True)
    ads_category = models.ForeignKey(AdsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Staff(DateTimeModel):
    name = models.CharField(max_length=50)
    post = models.CharField(max_length=40)
    profile = models.CharField(max_length=400,blank=True,null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Changed to CharField for flexibility
    DoB = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
