from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    number=models.IntegerField()
    description=models.TextField()

    def __str__(self):
        return self.email

class BlogPosts(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.TextField()
    author=models.CharField(max_length=50)
    img=models.ImageField(upload_to='blog', blank=True , null=True)
    timeStamp=models.DateTimeField(auto_now=True ,blank=True, null=True)

    def __str__(self):
        return self.author
     