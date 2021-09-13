from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class CharitySocialNetwork(admin.AdminSite):
    site_header = 'CHARITY SOCIAL NETWORK'


admin_site = CharitySocialNetwork(name='charity_admin')


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['avatar']

    def avatar(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=obj.image.name)
            )


class TagInlinePostAdmin(admin.StackedInline):
    model = Post.tags.through


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [TagInlinePostAdmin, ]


class LikeInlinePostAdmin(admin.StackedInline):
    model = Like
    fk_name = 'post'


class LikeAdmin(admin.ModelAdmin):
    list_display = ['updated_date', 'created_date', 'value', 'user', 'post']


class CommentInlinePostAdmin(admin.StackedInline):
    model = Comment
    fk_name = 'post'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_date', 'updated_date', 'user', 'post']


class PostContentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_date', 'updated_date', 'image', 'author']
    inlines = [TagInlinePostAdmin, LikeInlinePostAdmin, CommentInlinePostAdmin]
    form = PostContentForm


class ReportAdmin(admin.ModelAdmin):
    list_display = ['reason', 'image', 'reported_date', 'user_create_report', 'user_is_reported']


class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image', 'user_sell']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_date', 'started_price', 'last_price', 'items', 'user_buy']


admin_site.register(User, UserAdmin)
admin_site.register(Post, PostAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Like, LikeAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Report)
admin_site.register(AuctionItem)
admin_site.register(Transaction)

