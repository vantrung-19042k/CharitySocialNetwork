from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class CharitySocialNetwork(admin.AdminSite):
    site_header = 'CHARITY SOCIAL NETWORK'


# admin_site = CharitySocialNetwork(name='charity_admin')


class UserAdmin(admin.ModelAdmin):
    # readonly_fields = ['avatar']

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


class ActionInlinePostAdmin(admin.StackedInline):
    model = Action
    fk_name = 'post'


class ActionAdmin(admin.ModelAdmin):
    list_display = ['updated_date', 'created_date', 'type', 'creator', 'post']


class CommentInlinePostAdmin(admin.StackedInline):
    model = Comment
    fk_name = 'post'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_date', 'updated_date', 'creator', 'post']


class PostContentForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'content', 'created_date', 'updated_date', 'image', 'active', 'creator']
    inlines = [ActionInlinePostAdmin, CommentInlinePostAdmin]
    form = PostContentForm


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reason', 'image', 'reported_date', 'creator', 'user_is_reported']


class PriceInlineItemAdmin(admin.StackedInline):
    model = AuctionPrice
    fk_name = 'auction_item'


class AuctionPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'bidder']


class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'price', 'user_sell', 'post']
    inlines = [PriceInlineItemAdmin, ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_date', 'updated_date', 'started_price', 'last_price', 'item', 'user_buy']


admin.site.register(User, UserAdmin)

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(AuctionItem, AuctionItemAdmin)
admin.site.register(AuctionPrice, AuctionPriceAdmin)

admin.site.register(Report, ReportAdmin)
admin.site.register(Transaction, TransactionAdmin)
