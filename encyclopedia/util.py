import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import os

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def edit_entry(old_title, new_title, content):
    """
    Edits an entry, given its old title.
    Deletes old title entry and create a new entry with new title and content.
    Using this instead of save_entry ensures that two files will not be created
    when editing an old file with new title name.
    """
    old_filename = f"entries/{old_title}.md"
    new_filename = f"entries/{new_title}.md"
    if default_storage.exists(old_filename):
        default_storage.delete(old_filename)
    
    default_storage.save(new_filename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

