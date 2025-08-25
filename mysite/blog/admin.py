from django.contrib import admin
from blog.models import Category, Post, Gallery


# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    fk_name = 'post'
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    # def get_products_count(self, obj):
    #     if obj.posts:
    #         return str(len(obj.posts.all()))
    #     else:
    #         return '0'

    # get_products_count.short_description = 'Кол-во'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    inlines = (GalleryInline,)



admin.site.register(Category, CategoryAdmin),
admin.site.register(Post, PostAdmin)