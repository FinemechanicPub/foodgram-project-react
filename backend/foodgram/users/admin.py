from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from recipes.models import Favorite, ShoppingCart

from .models import Subscription, WebUser

admin.site.unregister(Group)


class FavoritesInline(admin.TabularInline):
    model = Favorite
    extra = 0


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0


class SubscriptionsInline(admin.TabularInline):
    model = Subscription
    fk_name = 'subscriber'
    readonly_fields = ('real_name',)
    extra = 0

    def real_name(self, subscription):
        author = subscription.author
        return f'{author.first_name} {author.last_name}'

    real_name.short_description = 'полное имя'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('subscriber__username', 'author__username')


@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_staff')
    list_display_links = ('username',)
    search_fields = ('email', 'username')
    inlines = (FavoritesInline, ShoppingCartInline, SubscriptionsInline)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
