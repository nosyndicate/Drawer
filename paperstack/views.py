# Create your views here.
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from datetime import date
from forms import SummaryCreateForm, SummaryBaseInfoForm, EditionForm
from models import Summary, Author, Keyword, Media, Area, Edition, Question
import urllib


        
def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name,args=args)
    params = urllib.urlencode(kwargs)
    print url+"?%s" % params
    return HttpResponseRedirect(url + "?%s" % params)


def get_media_str(media):
    return media.name + "-" + str(media.year.year)


def get_keywords_str(keywords):
    keyword_names = ""
    for k in keywords:
        keyword_names = keyword_names + k.__unicode__() + ";"
    return keyword_names

def get_areas_str(areas):
    area_names = ""
    for a in areas:
        area_names = area_names + a.__unicode__() + ";"
    return area_names


def get_authors_str(authors):
    author_names = ""
    for a in authors:
        author_names = author_names + a.__unicode__() + ";"
    return author_names




class IndexView(TemplateView):
    template_name="paperstack/index.html"
    
    
class SearchView(View):
    template_name="paperstack/search.html"
    
    def get(self, request, *args, **kwargs):
        key_string = request.GET['k'];
        keywords = self.get_keywords(key_string)
        result = Summary.objects.all()
        for k in keywords:
            result = result.filter(title__icontains=k)
            
        class Item:
            def __init__(self, id, title, authors, media):
                self.id = id
                self.title = title
                self.authors = authors
                self.media = media
        
        item_list = []
        for r in result:
            authors = r.author.all()
            author_names = ""
            for a in authors:
                author_names = author_names + a.__unicode__() + ";"
#             print author_names
            media = r.media.name + "-" + str(r.media.year.year)
#             print media
            item = Item(r.id,r.title,author_names,media)
            item_list.append(item)
            
        return render(request, self.template_name, {'item_list': item_list})
        
        
    def get_keywords(self, keyword):
        keywords = keyword.split(' ')
        return keywords








class SummaryCreateView(View):
    form_class = SummaryCreateForm(auto_id=False)
    template_name="paperstack/summary_create.html"
    

        
    def get_separate_name(self,name):
        names = name.split(" ")
        if len(names)==2:
            first = names[0]
            middle = ""
            last = names[1]
        elif len(names)==3:
            first = names[0]
            middle = names[1]
            last = names[2]
            
        return first, middle, last
    
    
    def get_media_field(self, media):
        fields = media.split("-")
        if len(fields)==2:
            name = fields[0]
            fullname = ""
            year = fields[1]
        elif len(fields)==3:
            name = fields[0]
            fullname = fields[1]
            year = fields[2]
        
        return name, fullname, year
    
    
    def get_summary_id(self, title):
        result = Summary.objects.filter(title=title)
#         print "start to print result"
#         print result
        
        
        r = list(result[:1])
        if r:
            return r[0].id
        else:
            return -1;
        
        

    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        #form = SummaryCreateForm(request.POST)
        
        authors = request.POST["authors"]
        keywords = request.POST["keywords"]
        summary_title = request.POST["title"]
        media = request.POST["media"]
        areas = request.POST["areas"]
        summary = request.POST["summary"]
        questions = request.POST["questions"]
        
        summary_id = self.get_summary_id(summary_title)
        if summary_id!=-1:
#             print "we have this summary"
            return custom_redirect("paperstack:browse",id=summary_id)
            #return HttpResponseRedirect(reverse('paperstack:browse',args=(summary_id,))) # Redirect after POST
            
        
        
        authors = authors.split(";")
        author_objs = []
        for author in authors:
            first, middle, last = self.get_separate_name(author)
            object, create = Author.objects.get_or_create(firstname=first,middlename=middle,lastname=last)
            author_objs.append(object)
   
#         print author_objs
          
        keywords = keywords.split(";")
        keyword_objs = []
        for k in keywords:
            object, create = Keyword.objects.get_or_create(keyword=k)
            keyword_objs.append(object)
          
#         print keyword_objs
          
        n, f, y = self.get_media_field(media)
        object, create = Media.objects.get_or_create(name=n,full_name=f,year=date(int(y),1,1))
        media_obj = object
          
        areas = areas.split(";")
        area_objs = []
        for a in areas:
            object, create = Area.objects.get_or_create(label=a)
            area_objs.append(object)
          
#         print area_objs
          
          
        edit_content = summary
        #media is the foreign key of summary, so we create summary from media
        summary = media_obj.summary_set.create(title=summary_title)
        for a in author_objs:
            summary.author.add(a)
        for k in keyword_objs:
            summary.keyword.add(k)
        for a in area_objs:
            summary.area.add(a)
          
          
        edition = summary.edition_set.create(content=edit_content)
          
        questions = questions.split("?")
        for q in questions:
            if(q!=""):
                question_obj = edition.question_set.create(question=q)
        
        return custom_redirect("paperstack:browse",id=summary.id)
        #return HttpResponseRedirect(reverse('paperstack:browse',args=(summary.id,))) # Redirect after POST





class SummaryBrowseView(View):
    template_name = "paperstack/summary_browse.html"
    
    def get(self, request, *args, **kwargs):
        
        summary_id = request.GET["id"]
        
        summary = get_object_or_404(Summary, pk=summary_id)
        
        class BaseInfo:
            def __init__(self,title,authors,media,areas,keywords):
                self.title = title
                self.authors = authors
                self.media = media
                self.areas = areas
                self.keywords = keywords
                
        authors = summary.author.all()
        author_names = get_authors_str(authors)

        media = get_media_str(summary.media)

        areas = summary.area.all()
        area_names = get_areas_str(areas)

        keywords = summary.keyword.all()
        keyword_names = get_keywords_str(keywords)

        base_info = BaseInfo(summary.title,author_names,media,area_names,keyword_names)
        
        
        edition_list = summary.edition_set.all()
        
        edit_infos = []
        
        class EditInfo:
            def __init__(self,id,content,time,questions):
                self.id = id
                self.content = content
                self.time = time
                self.questions = questions
        

        for e in edition_list:
            questions = e.question_set.all()
            question_set = []
            for q in questions:
                question_set.append(q.question+"?")
            edit_info = EditInfo(e.id,e.content,e.edit_time,question_set)
            edit_infos.append(edit_info)
        
        kwargs = {
            "summary_id":summary_id,
            "base_info": base_info,
            "edit_infos":edit_infos
        }
        
        return render(request, self.template_name,kwargs)
    



class BaseInfoEditView(View):

    template_name="paperstack/baseinfo_edit.html"
    
    
    def get_field(self, summary):
        
        title = summary.title
        
        authors = summary.author.all()
        authors = get_authors_str(authors)

        media = get_media_str(summary.media)

        areas = summary.area.all()
        areas = get_areas_str(areas)

        keywords = summary.keyword.all()
        keywords = get_keywords_str(keywords)
        
        
        return title, authors, media, areas, keywords
    
    def get(self, request, *args, **kwargs):

        summary_id = request.GET["summary_id"]
        
        summary = Summary.objects.get(pk=summary_id)
        
        title, authors, media, areas, keywords = self.get_field(summary)

        data = {
            "title":title,
            "authors":authors,
            "media":media,
            "areas":areas,
            "keywords":keywords
        }
        
        form = SummaryBaseInfoForm(data,auto_id=False)
        

        return render(request, self.template_name, {'form':form,"summary_id":summary_id})
    
    def post(self, request, *args, **kwargs):
        
        authors = request.POST["authors"]
        keywords = request.POST["keywords"]
        summary_title = request.POST["title"]
        media = request.POST["media"]
        areas = request.POST["areas"]
        summary_id = request.POST["summary_id"]
        
        summary = Summary.objects.get(pk=summary_id)
        
        summary.title = summary_title
        
        summary.save()
    
class EditionView(View):

    template_name="paperstack/edition.html"
    
    def get_field(self,edition):
        content = edition.content
        
        questions = edition.question_set.all()
        question_set = ""
        for q in questions:
            question_set = question_set + q.question + "?"
        
        return content, question_set
    
    
    def init_value(self,edition_id):
        edition = Edition.objects.get(pk=edition_id)
        
        content, question_set = self.get_field(edition)

        data = {
            "summary":content,
            "questions":question_set,
        }
        
        form = EditionForm(data,auto_id=False)
        
        return form
    
    
    
    def get(self, request, *args, **kwargs):

        summary_id = request.GET["summary_id"]
        edition_id = request.GET["edition_id"]
        
        print "summary_id is"
        print summary_id
         
        print "edition_id is"
        print edition_id
        
        label = ""
        
        if int(summary_id) == -1:
            label = "Update"
            form = self.init_value(edition_id)
        
        if int(edition_id) == -1:
            label = "Add"
            form = EditionForm(auto_id=False)


        
        return render(request, self.template_name, {"form":form,"label":label,"edition_id":edition_id})
    
    def post(self, request, *args, **kwargs):
        summary = request.POST["summary"]
        questions = request.POST["questions"]
        edition_id = request.POST["edition_id"]
        
        edition = Edition.objects.get(pk=edition_id)
        edition.content = summary
        edition.save()
        
        #delete all original question
        edition.question_set.all().delete()
        
        print questions
        if(questions!=""):
            questions = questions.split("?")
            for q in questions:
                if(q!=""):
                    question_obj = edition.question_set.create(question=q)
        
        summary_id = edition.summary.id
        
        return custom_redirect("paperstack:browse",id=summary_id)
        


