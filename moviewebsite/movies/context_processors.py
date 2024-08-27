# movies/context_processors.py
from .models import Category

def category_list(request):
    return {
        'categories': Category.objects.all()
    }