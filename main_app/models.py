from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

STATUSS = (
    ('E', 'Employed'),
    ('U', 'Unemployed'),
    ('A', 'Applying')
)


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    notes = models.TextField(max_length=150)

    def __str__(self):
        return f'{self.notes} {self.company} {self.email} {self.name}'

    def get_absolute_url(self):
        return reverse('contacts_detail', kwargs={'pk': self.id})


class Profile(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    age = models.IntegerField()
    aboutme = models.TextField(max_length=250)
    contacts = models.ManyToManyField(Contact)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def post_for_today(self):
        return self.posting_set.filter(date=date.today()).count() >= len('1')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})

class Posting(models.Model):
    date = models.DateField('posting date')
    status = models.CharField(
        max_length=1,
        choices=STATUSS,
        default=STATUSS[0][0]
    )
    text = models.TextField(max_length=250)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_status_display()} on {self.date}"

    class Meta: 
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"