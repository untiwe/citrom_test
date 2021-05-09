from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
# Create your views here.
# python manage.py makemigrations
# python manage.py migrate

# def image_upload_view(request):
#     return render(request, "add_post/add_post.html")


def add_post(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'add_post/add_post.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()

    return render(request, 'add_post/add_post.html', {'form': form})


def img(request):

    if request.method == 'POST':

        print(request.FILES)
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():

            # location = Image.objects.create(
            #     title=request.user, image=form.cleaned_data['name'])
            # for f in request.FILES.getlist('photos'):
            #     print("   ")
            #     print(f)
            #     print("   ")
            #     # data = f.read()  # Если файл целиком умещается в памяти
            #     photo = Image(location=image)
            #     photo.image.save(f.name)  # , ContentFile(data))
            #     photo.save()
            #     # Надо определить get_absolute_url() в модели
            return render(request, 'add_post/img.html', {'form': form})

    form_class = FileFieldForm()
    return render(request, 'add_post/img.html', {'form': form_class})
