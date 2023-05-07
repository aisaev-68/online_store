from .models import Catalog, Category


def catalogs(request):
    """
    Контекстный процессор для каталога.
    """
    catalog = Catalog.objects.all()

    return {
        'catalogs': catalog,
    }