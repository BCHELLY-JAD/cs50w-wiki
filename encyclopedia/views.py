from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import markdown2
from django.urls import reverse
import random as rdm
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#specification 1: Entry-page

def entries(request, name):
    content = util.get_entry(name)

    if content is not None: 
        converted_code = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", { 
            "entry": converted_code,
            "title": name
        })
 
    else: 
        return render(request, "encyclopedia/error.html", { 
            "error": f"Showing results for '{name}'. No results found for '{name}'!"
        })


#specification 3: search

def search(request): 
    if request.method == 'POST': 
        response = request.POST["q"]
        text = util.get_entry(response)
        if text: 
            return HttpResponseRedirect("wiki/"+response)
        else: 
            entries = util.list_entries()
            search_entries = [ i for i in entries if response in i]
            if search_entries: 
                return render(request, 'encyclopedia/index.html', { 
                    "entries" : search_entries
                })
            else: 
                return render(request, "encyclopedia/error.html", { 
                    "error": "The page you are looking for does not exist"
                    })


# specification 4: New Page

def add(request):
    if request.method == "POST":
        name = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()
        if name in entries: 
            return render(request, "encyclopedia/error.html", { 
                "error": "This page already exists"
            })
        else: 
            util.save_entry(name, content)
            return HttpResponseRedirect("wiki/"+name)     

    return render(request, "encyclopedia/newPage.html")

#specification 5: Edit Page

def edit(request, title):
    if request.method=="GET":    
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                    "title": title,
                    "content": content
            })


def save(request, title):
    fileText = request.POST["content"]
    util.save_entry(title, fileText)
    return HttpResponseRedirect(reverse('entries', args=(title,)))

#specification 6: Random Page

def random(request):
    entries=util.list_entries()
    randomChoice=rdm.choice(entries)
    return HttpResponseRedirect("wiki/"+randomChoice)