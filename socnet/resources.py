from import_export import resources
from socnet.models import Post


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = ['page__shtab__name', 'url', 'posted_on','title', 'description', 'views' ]
