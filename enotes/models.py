from django.contrib.auth.models import User
from django.db import models


class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ContactNo = models.CharField(max_length=10, null=True)
    About = models.CharField(max_length=450, null=True)
    Role = models.CharField(max_length=150, null=True)
    RegDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
    categoryName = models.CharField(max_length=150, null=True)
    CreationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoryName


class Notes(models.Model):
        signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
        category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
        noteDescription = models.CharField(max_length=250, null=True)
        CreationDate = models.DateTimeField(auto_now_add=True)
        UpdationDate = models.DateField(null=True)
        is_important = models.BooleanField(default=False)
        tags = models.CharField(max_length=250, null=True)

        def __str__(self):
            return self.noteDescription


class Noteshistory(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, null=True)
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
    noteDetails = models.CharField(max_length=250, null=True)
    postingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.noteDetails
