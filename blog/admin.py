from django.contrib import admin
from blog.models import Post, Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['name']})
    ]
    
    list_display = ('name', 'created_on', 'updated_on')
    
    search_fields = ["name"]

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'slug', 'summary', 'content',
            'is_published', 'publish_date', 'tags']})
    ]
    
    list_display = ('title', 'author', 'is_published', 'publish_date',
        'created_on', 'updated_on')
    
    prepopulated_fields = {'slug': ('title',), }
    
    search_fields = ["title"]

    def save_model(self, request, obj, form, change):
        if not obj in Post.objects.all():
            obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)