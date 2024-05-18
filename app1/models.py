from django.db import models

# Create your models here.


class UsersManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 charters"
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 charters"
        if len(post_data["password1"]) < 8:
            errors["password1"] = "Password should be at least 8 charters"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank=True)

    objects = UsersManger()


class Team(models.Model):
    name = models.CharField(max_length=255)


class IDeaManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data["idea_text"]) < 5:
            errors["idea_text"] = "Idea should have 5 or more characters"
        return errors


class Idea(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = IDeaManger()
