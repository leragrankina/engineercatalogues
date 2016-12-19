from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET['next'])
        return render(request, 'registration/login.html', {'error': 'Неправильный логин или пароль'})


@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'registration/change_pass.html')
    if request.method == 'POST':
        username = request.user.username
        old_password = request.POST.get('old-password', False)
        user = User.objects.get(username__exact=username)
        if user.check_password(old_password):
            new_password = request.POST.get('new-password', False)
            if new_password:
                if len(new_password) > 7:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    return render(request, 'registration/change_success.html')
                else:
                    return render(request, 'registration/change_pass.html', {'error': 'Пароль слишком короткий'})
            else:
                return render(request, 'registration/change_pass.html', {'error': 'Новый пароль должен быть заполнен'})
        else:
            return render(request, 'registration/change_pass.html', {'error':'Старый пароль %s не подходит' % old_password})
