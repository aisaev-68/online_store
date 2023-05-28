from django.shortcuts import render

def error_403(request, reason=''):
    return render(request, 'frontend/error.html', {'path': request.path, 'error_text': 'Доступ к запрошенному ресурсу запрещен'})

def error_404(request, exception):
    return render(request, 'frontend/error.html', {'path': request.path, 'error_text': 'Страница не найдена'}, status=404)

def error_500(request):
    return render(request, 'frontend/error.html', {'path': request.path, 'error_text': 'Ошибка сервера'}, status=500)
