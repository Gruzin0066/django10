from django.contrib import admin
from blog.models import Category, Post, Gallery, PostTags


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
    list_display = ('title', 'slug','category', 'is_published')
    list_filter = ('is_published', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('category', 'is_published')
    inlines = (GalleryInline,)


class PostTagsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')
    list_display_links = ('tag', 'slug')
    prepopulated_fields = {'slug': ('tag',)}



admin.site.register(Category, CategoryAdmin),
admin.site.register(Post, PostAdmin)
admin.site.register(PostTags, PostTagsAdmin)