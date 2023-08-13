from django.contrib import admin
from socnet.models import Tguser,Page,Platform,Post,Shtab,Pagestat
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from rangefilter.filter import DateRangeFilter
from import_export.admin import ExportMixin

def format(obj):
    return format_html('<a href="{}" target="_blank">{}</a>',obj.url, obj.url)


class PostInline(admin.TabularInline):
    model = Post
    ordering = ("-posted_on",)
    readonly_fields = ['post_id', 'posted_on', 'link',
                       'views', 'likes', 'reposts', 'comments']
    can_delete = False                   
    extra = 0

    def link(self, obj):
        return format(obj)  


class PageInline(admin.TabularInline):
    model = Page
    readonly_fields = ['full_name','platform', 'link', 
                       'followers_count', 'last_post_date',]
    exclude = ['notifs','feed_id','username',]
    extra = 0
    show_change_link = True
    can_delete = False

    def link(self, obj):
        return format(obj)

    def last_post_date(self, obj):
        try:
            return str(last_posted_on)[:10]
        except:
            return None


class PagestatInline(admin.TabularInline):   
    model = Pagestat          
    extra = 0
    readonly_fields = ['date', 'followers_count']
    can_delete = False
    classes = ['collapse']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username', 'feed_id', ]
    list_display = ['shtab', 'platform', 
                    'followers_count', 'is_subscribed', 'link',]
    list_filter = ['platform', 'shtab',]
    filter_horizontal = ('notifs',)
    readonly_fields = ['link', 'last_post_id', 
                       'followers_count', 'feed_id', 'full_name',]
    actions = ['subscribe','unsubscribe']
    inlines = [
        PagestatInline,
        PostInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def link(self, obj):
        return format(obj)

    def is_subscribed(self, obj):
        return self.request.user.tguser in obj.notifs.all()    
    is_subscribed.boolean = True
    is_subscribed.short_description = "I'm subscribed"

    def subscribe(self, request, queryset):
        for page in queryset:
            page.notifs.add(request.user.tguser)
    subscribe.short_description = "Subscribe"

    def unsubscribe(self, request, queryset):
        for page in queryset:
            page.notifs.remove(request.user.tguser)
    unsubscribe.short_description = "Unubscribe"

    
    #search_fields = ['username', 'first_name', 'last_name']
    #readonly_fields =  ['tg_id', 'username', 'first_name', 'last_name',
    #                    'auth_date', 'source']

    

@admin.register(Tguser)
class PageAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'username']

    def username(self, obj):
        try:
            return obj.user.username
        except:
            return None 
    username.short_description = 'Username'


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Shtab)
class ShtabAdmin(admin.ModelAdmin):
    exclude = ['url']
    list_display = ['name', 'is_open']   
    list_filter = ['is_open'] 
    ordering = ['name',]
    inlines = [
        PageInline,
    ]

    def Site(self, obj):
        return obj.page_set.filter(platform=Platform.SI).exists()
    Site.boolean = True

    def Vk(self, obj):
        return obj.page_set.get(platform=Platform.VK).followers_count
    
    def Instagram(self, obj):
        return obj.page_set.get(platform=Platform.IN).followers_count

    def Twitter(self, obj):
        return obj.page_set.get(platform=Platform.IN).followers_count

    def Facebook(self, obj):
        return obj.page_set.get(platform=Platform.FB).followers_count

    def OK(self, obj):
        return obj.page_set.filter(platform=Platform.OK).exists()
    OK.boolean = True

    def link(self, obj):
        return format(obj) 


@admin.register(Post)
class PostAdmin(ExportMixin, admin.ModelAdmin):
    readonly_fields = ['shtab', 'platform', 'link', 
                       'views', 'likes', 'reposts', 'comments','posted_on',]

    list_display = ['shtab', 'platform', 'link', 
                    'views', 'likes', 'reposts', 'comments','posted_date',]

    list_filter = ['page__platform', ('posted_on',DateRangeFilter), 
                   'page__shtab', ]

    date_hierarchy = 'posted_on'

    def link(self, obj):
        return format(obj) 

    def shtab(self, obj):
        return obj.page.shtab.name
    
    def platform(self, obj):
        return obj.page.platform.name    

    def posted_date(self, obj):
        try: 
            return obj.posted_on.date() 
        except:
            return None    

    