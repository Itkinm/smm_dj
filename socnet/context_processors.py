from socnet.models import Platform, Shtab

def add_navbar(request):
    shtab_qs = Shtab.objects.filter(is_open = True).exclude(url=None).order_by('name')
    shtabs = [x.page_set.get(platform = Platform.SI) for x in shtab_qs]
    return {
        'platforms': Platform.objects.filter(hook = True),
        'shtabs': shtabs
    }