from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .forms import AuthorForm, AddResearchForm
from .models import Publication, Author
from django.http import JsonResponse
from django.template.loader import render_to_string

def add(request):
    if request.method == 'POST':
        p_id = request.POST.get("p_id", "")
        if(p_id):
            rec=Publication.objects.get(id=p_id)
            add=AddResearchForm(request.POST,instance=rec)
            msg="The publication has been edited successfully"
        else:
            add=AddResearchForm(request.POST)
            msg = "The publication has been added successfully"
        if(add.is_valid()):
            add.save()
        return render(request, 'add_research.html', {'form':add,'id':p_id,'msg':msg})
    else:
        add = AddResearchForm()
        return render(request, 'add_research.html', {'form': add})


def index(request):
    return render(request, 'index.html', {'pubs':Publication.objects.all().order_by('year_of_publication')})

def search(request):
    keyword = request.GET.get('keyword', None)
    pubs = Publication.objects.all().filter(title__contains=keyword)
    context = {
        'pubs':pubs
    }
    data = {'rendered_table': render_to_string('publications.html', context=context)}

    return JsonResponse(data)


def year_wise(request,year):    
    return render(request, 'index.html', {'pubs':Publication.objects.all().filter(year_of_publication=year)})

def author_wise(request,author):
    return render(request, 'index.html', {'pubs':Publication.objects.all().filter(authors__last_name =author)})

def edit(request,p_id=1):
    p = Publication.objects.get(pk=p_id)
    add = AddResearchForm(instance=p)
    return render(request, 'add_research.html', {'form':add,'id':p_id})

def delete(request,p_id=1):
    p = Publication.objects.get(pk=p_id)
    p.delete()
    return render(request, 'index.html', {'pubs': Publication.objects.all().order_by('year_of_publication'),'msg':"The publication has been deleted successfully"})

def add_author(request):
    if request.method == 'GET':
        form = AuthorForm()		
        return render(request,'add_author.html', {'form': form})
    else:
        auth_id = request.POST['author_id']
        instance = None
        try:
            instance = Author.objects.get(author_id=auth_id)
        except Author.DoesNotExist:
            instance=None
        form = AuthorForm(request.POST or None, instance=instance)
        if(form.is_valid()):
            form.save()
            return render(request,'add_author.html', {'form': form,  'message': 'Author has been saved'})
        else:
            print("Form errors " , form.errors)
            return render(request,'add_author.html', {'form': form, 'message': 'Unable to save author'})