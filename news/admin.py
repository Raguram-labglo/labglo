from django.contrib import admin
from news.models import Tag, News

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['name']})
    ]
    
    list_display = ('name', 'created_on', 'updated_on')
    
    search_fields = ["name"]

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'slug', 'is_active', 'description',
            'image_url', 'source', 'tag' ]})
    ]
    
    list_display = ('title', 'is_active', 'created_on', 'updated_on')
    
    search_fields = ["slug"]

    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)