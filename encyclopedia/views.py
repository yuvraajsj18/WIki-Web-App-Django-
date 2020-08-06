import re
import random
from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown

from . import util



# displays home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


# display entry page of the given entry
def entry_page(request, title):
    # get content from the entry
    entry_content = util.get_entry(title)

    # check if entry is present or not
    if entry_content == None:
        return render(request, "encyclopedia/errors/notfound.html")
    

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_content": markdown(entry_content, safe_mode = "escape"),
    })


# search for a given entry if found display that entry otherwise display matched results
def search(request):
    query = str(request.GET["q"])
    
    # entry exist then redirect to entry_page
    if util.get_entry(query.title()):
        return HttpResponseRedirect(reverse('encyclopedia:entry_page', args=[query.title()]))

    entries = util.list_entries()

    # find similar entries - case insensitive search with lowercase
    results = [entry for entry in entries if query.lower() in entry.lower() or entry.lower() in query.lower()]

    return render(request, 'encyclopedia/searchresult.html', {
        "query": query,
        "results": results,
    })


# adds new page in the disk by taking input from the user
def new_page(request):
    if request.method == "POST":
        title = str(request.POST["title"])
        content = str(request.POST["content"])

        # if page already exist then show error
        all_entries = [entry.lower() for entry in util.list_entries()]
        if title.lower() in all_entries:
            return render(request, 'encyclopedia/errors/alreadyexist.html', {
                "title": title.capitalize(),
            })

        # add page to the disk and take user to the new page
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse('encyclopedia:entry_page', args=[title]))     
    else:
        return render(request, 'encyclopedia/newpage.html')

# display a page for editing and edit it on POST request
def edit_page(request, title):
    if request.method == "POST":
        new_title = str(request.POST["title"])
        new_content = str(request.POST["content"])

        # add page to the disk and take user to the new page
        # Using util.edit() instead of save_entry ensures that two files will not be created
        # when editing an old file with new title name.
        util.edit_entry(title, new_title, new_content)

        return HttpResponseRedirect(reverse('encyclopedia:entry_page', args=[new_title]))
    else:
        content = util.get_entry(title)

        return render(request, 'encyclopedia/editpage.html', {
            "title": title,
            "content": content,
    })

def random_page(request):
    titles = util.list_entries()
    # if no title exist no random can be displayed
    if len(titles) == 0:
        return render(request, 'encyclopedia/notfound.html')
    
    # select a random title
    random_title = random.choice(titles)

    # redirect to entry page of random title
    return HttpResponseRedirect(reverse('encyclopedia:entry_page', args = [random_title]))