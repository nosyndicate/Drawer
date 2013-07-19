from django.db import models

# Create your models here.
class Area(models.Model):
    parent = models.ForeignKey('self',null=True,blank=True)
    label = models.CharField(max_length=50)
    

    def __unicode__(self):
        return self.label




class Keyword(models.Model):
    keyword = models.CharField(max_length=30)

    def __unicode__(self):
        return self.keyword

class Author(models.Model):
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)

    def __unicode__(self):
        fullname = self.firstname + ' ' + self.middlename + ' ' + self.lastname
        return fullname


class Media(models.Model):
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    year = models.DateField()

    def __unicode__(self):
        return self.name + '-' + self.year.__str__()



class Summary(models.Model):
    author = models.ManyToManyField(Author)
    keyword = models.ManyToManyField(Keyword)
    area = models.ManyToManyField(Area)
    media = models.ForeignKey(Media)
    title = models.CharField(max_length=100)
    

    def __unicode__(self):
        return self.title



class Edition(models.Model):
    summary = models.ForeignKey(Summary)
    edit_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return self.edit_time


class Question(models.Model):
    edition = models.ForeignKey(Edition)
    question = models.TextField()

    def __unicode__(self):
        return self.question
 
    
