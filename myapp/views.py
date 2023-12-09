import base64
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'loginindex.html')

def login_post(request):
    a=request.POST['username']
    b=request.POST['password']
    result=Login.objects.filter(username=a,password=b)
    if result.exists():
        result2=Login.objects.get(username=a,password=b)
        request.session['lid']=result2.id
        if result2.type=='admin':
            return HttpResponse('''<script>alert('Admin login success fully');window.location='/myapp/admin_home/'</script>''')

        elif result2.type=='theatre':
            return HttpResponse('''<script>alert('Theatre login success fully');window.location='/myapp/theatre_home/'</script>''')


        else:
            return HttpResponse(
                '''<script>alert('invalid');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('invalid');window.location='/myapp/login/'</script>''')


def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert('Logout');window.location='/myapp/login/'</script>''')


def admin_home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'admin/admin_home2.html')


def admin_change_password(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'admin/Admin_change_password.html')


def admin_change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')

def view_premium_users(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=User.objects.filter(type='premium')
    return render(request,'admin/view_premium_user.html',{'data':var})

def view_premium_users_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search=request.POST['search']
    var=User.objects.filter(name__icontains=search)
    return render(request,'admin/view_premium_user.html',{'data':var})


# def aprove_premium(request,id):
#
#     return HttpResponse('''<script>alert(' Aprove SuccessFully');window.location='/myapp/view_premium_users/'</script>''')


def view_theatre(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre.objects.filter(status='pending')
    return render(request,'admin/admin_view_theatre.html',{'data':var})

def view_theatre_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['searching']
    var = Theatre.objects.filter(name__icontains=search)
    return render(request,'admin/admin_view_theatre.html',{'data':var})

def reject_theatre(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    Theatre.objects.filter(LOGIN_id=id).update(status='rejected')
    Login.objects.filter(id=id).update(type='pending')

    return HttpResponse('''<script>alert('Theatre Reject');window.location='/myapp/view_reject_theatre/'</script>''')


def aproving_theatre(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    Theatre.objects.filter(LOGIN_id=id).update(status='approved')
    Login.objects.filter(id=id).update(type='theatre')


    return HttpResponse('''<script>alert('Theatre Approved');window.location='/myapp/view_aproved_theatre/'</script>''')


def view_aproved_theatre(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre.objects.filter(status='approved')
    return render(request,'admin/view_aproved_theatre.html',{'data':var})

def view_aproved_theatre_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['searching']
    var = Theatre.objects.filter(name__icontains=search)
    return render(request,'admin/admin_view_theatre.html',{'data':var})


def view_reject_theatre(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre.objects.filter(status='rejected')
    return render(request,'admin/view_rejected_theatre.html',{'data':var})

def view_reject_theatre_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['searching']
    var = Theatre.objects.filter(name__icontains=search)
    return render(request,'admin/view_rejected_theatre.html',{'data':var})

def view_user(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=User.objects.all()
    return render(request,'admin/view__user.html',{'data':var})

def view_user_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['search']
    var = User.objects.filter(name__icontains=search)
    return render(request,'admin/view__user.html',{'data':var})

def view_review_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Theatre_review.objects.filter(date__range=[fromdate,to])
    return render(request,'admin/view_review.html',{'data':var})

def view_theatre_review(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre_review.objects.all()
    return render(request,'admin/view_review.html',{'data':var})

def movie_review(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie_review.objects.all()
    return render(request,'admin/movie_view_review.html',{'data':var})

def movie_review_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Theatre_review.objects.filter(date__range=[fromdate,to])
    return render(request,'admin/movie_view_review.html',{'data':var})


def view_complaint(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Complaint.objects.all()
    return render(request, 'admin/View_complaint.html',{'var':var})



def view_complaint_post(request, ):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromD=request.POST['f']
    to=request.POST['t']
    var=Complaint.objects.filter(date__range=[fromD,to])

    return render(request, 'admin/View_complaint.html', {'var': var})



def complaint_reply(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Complaint.objects.get(id=id)

    return render(request,'admin/complaint_reply.html',{'data':var})


def complaint_reply_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    id = request.POST['id']
    com = request.POST['reply']
    date=datetime.now().date().today()
    var = Complaint.objects.get(id=id)
    var.reply = com
    var.status = 'Replied'
    var.dat=date
    var.save()
    return HttpResponse('''<script>alert('successfully sent');window.location='/myapp/view_complaint/'</script>''')


def add_movie(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'admin/add_movie.html')


def add_movie_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    name = request.POST['name']
    duration = request.POST['duration']
    language = request.POST['language']
    production_name = request.POST['production_name']
    cast = request.POST['cast']
    producer_name = request.POST['producer_name']
    directior_name = request.POST['directior_name']
    gentre = request.POST['gentre']

    trailer=request.FILES['trailer']
    date = datetime.now().strftime("%Y%m%d-%H%M%S")+'.mp4'
    fs = FileSystemStorage()
    fs.save(date,trailer)
    path = fs.url(date)

    poster=request.FILES['poster']
    date1 = datetime.now().strftime("%Y%m%d-%H%M%S")+'.jpg'
    fs1 = FileSystemStorage()
    fs1.save(date1,poster)
    path1 = fs1.url(date1)

    certificate = request.FILES['certificate']
    date2 = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
    fs2 = FileSystemStorage()
    fs2.save(date2,certificate)
    path2 = fs2.url(date2)

    var=Movie()
    var.name=name
    var.duration=duration+'/Hours'
    var.language=language
    var.cast_and_crew=cast
    var.production_house_name=production_name
    var.producer_name=producer_name
    var.director_name=directior_name
    var.gentre=gentre
    var.trailer=path
    var.poster=path1
    var.certificate=path2
    var.save()



    return HttpResponse('''<script>alert('Movie Added');window.location='/myapp/add_movie/'</script>''')

def view_movies(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie.objects.all()
    return render(request,'admin/view_movie.html',{'data':var})

def view_movies_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search=request.POST['search']
    var=Movie.objects.filter(name__icontains=search)
    return render(request,'admin/view_movie.html',{'data':var})


def movies_delete(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('Movie Deleted');window.location='/myapp/view_movies/'</script>''')

def edit_movie(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie.objects.get(id=id)
    return render(request,'admin/edit_movie.html',{'data':var})


def edit_movie_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    id = request.POST['id']
    name = request.POST['name']
    duration = request.POST['duration']
    language = request.POST['language']
    production_name = request.POST['production_name']
    cast = request.POST['cast']
    producer_name = request.POST['producer_name']
    directior_name = request.POST['directior_name']
    gentre = request.POST['gentre']



    var=Movie.objects.get(id=id)
    var.name=name
    var.duration=duration
    var.language=language
    var.cast_and_crew=cast
    var.production_house_name=production_name
    var.producer_name=producer_name
    var.director_name=directior_name
    var.gentre=gentre


    if 'trailer' in request.FILES:
        trailer = request.FILES['trailer']
        if trailer.name != '':
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, trailer)
            path = fs.url(date)
            var.trailer = path

    if 'certificate' in request.FILES:
        certificate = request.FILES['certificate']
        if certificate.name !='':
            date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
            fs1 = FileSystemStorage()
            fs1.save(date1, certificate)
            path1 = fs1.url(date1)
            var.certificate = path1

    if 'poster' in request.FILES:
        poster = request.FILES['poster']
        if poster.name !='':
            date2 = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
            fs2 = FileSystemStorage()
            fs2.save(date2, poster)
            path2 = fs2.url(date2)
            var.poster=path2
    var.save()

    return HttpResponse('''<script>alert('Movie Updated');window.location='/myapp/view_movies/'</script>''')

# theatre#


def theatre_home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'theatre/theatre_home2.html')


def add_theatre(request):

    return render(request, 'signupindex.html')



def add_theatre_post(request):


    name=request.POST['name']
    place=request.POST['place']
    pin=request.POST['pin']
    city=request.POST['city']
    ownername=request.POST['ownername']
    phone=request.POST['phone']
    established=request.POST['established']
    email=request.POST['email']
    working_time=request.POST['working_time']
    about=request.POST['about']
    password=request.POST['password']
    confirm=request.POST['confirm']


    photo=request.FILES['photo1']
    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)




    if password==confirm:
        var = Login()
        var.username = email
        var.password = password
        var.type='pending'
        var.save()

        var2=Theatre()
        var2.LOGIN=var
        var2.name=name
        var2.place=place
        var2.pin=pin
        var2.city=city
        var2.ownername=ownername
        var2.phone=phone
        var2.established=established
        var2.ownername=ownername
        var2.email=email
        var2.working_time=working_time
        var2.about=about
        var2.photo=path
        var2.status='pending'
        var2.save()
        return HttpResponse('''<script>alert('Theatre Regitered');window.location='/myapp/add_theatre/'</script>''')
    else:
        return HttpResponse('''<script>alert('Password Not Same');window.location='/myapp/add_theatre/'</script>''')




def theatre_profile(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre.objects.get(LOGIN=request.session['lid'])
    return render(request,'theatre/theatre_profile.html',{'data':var})


def edit_theatre(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre.objects.get(id=id)
    return render(request,'theatre/edit_theatre.html',{'i':var})

def edit_theatre_post(request,):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    id=request.POST['id']
    name = request.POST['name']
    place = request.POST['place']
    pin = request.POST['pin']
    city = request.POST['city']
    ownername = request.POST['ownername']
    phone = request.POST['phone']
    established = request.POST['established']
    email = request.POST['email']
    working_time = request.POST['working_time']
    about = request.POST['about']



    var2 = Theatre.objects.get(id=id)
    var2.name = name
    var2.place = place
    var2.pin = pin
    var2.city = city
    var2.ownername = ownername
    var2.phone = phone
    var2.established = established
    var2.ownername = ownername
    var2.email = email
    var2.working_time = working_time
    var2.about = about

    if 'photo1' in request.FILES:
        photo = request.FILES['photo1']
        if photo.name!='':
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            var2.photo = path
    var2.save()





    return HttpResponse('''<script>alert('Updated');window.location='/myapp/theatre_profile/'</script>''')

def theatre_view_movies(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie.objects.all()

    return render(request,'theatre/theatre_view_movies.html',{'data':var})

def theatre_view_movies_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')



    search=request.POST['search']
    var=Movie.objects.filter(name__icontains=search)
    return render(request,'theatre/theatre_view_movies.html',{'data':var})


def add_screen(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'theatre/add_screen.html')


def add_screen_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')


    lid=request.session['lid']
    size=request.POST['size']
    screen_number=request.POST['screen_number']
    audio_quality=request.POST['audio_quality']
    audio_type=request.POST['audio_type']
    seat_charge=request.POST['seat_charge']
    total_set=request.POST['total_set']

    var=Screen()
    var.THEATRE=Theatre.objects.get(LOGIN=lid)
    var.size=size +'/Inches'
    var.screen_number=screen_number
    var.audio_type=audio_type
    var.seat_charge=seat_charge
    var.total_set=total_set
    var.audio_quality=audio_quality
    var.save()

    return HttpResponse('''<script>alert('Screen Added');window.location='/myapp/add_screen/'</script>''')



def theatre_view_screen(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Screen.objects.all()
    return render(request,'theatre/theatre_view_screen.html',{'data':var})

def theatre_view_screen_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['search']
    var = Screen.objects.filter(screen_number__icontains=search)
    return render(request,'theatre/theatre_view_screen.html',{'data':var})


def delete_screen(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Screen.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('Screen Deleted');window.location='/myapp/theatre_view_screen/'</script>''')

def edit_screen(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Screen.objects.get(id=id)
    return render(request,'theatre/edit_screen.html',{'i':var})

def edit_screen_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')


    id=request.POST['id']
    size=request.POST['size']
    screen_number=request.POST['screen_number']
    audio_quality=request.POST['audio_quality']
    audio_type=request.POST['audio_type']
    seat_charge=request.POST['seat_charge']
    total_set=request.POST['total_set']

    var=Screen.objects.get(id=id)
    var.size=size
    var.screen_number=screen_number
    var.audio_type=audio_type
    var.seat_charge=seat_charge
    var.total_set=total_set
    var.audio_quality=audio_quality
    var.save()

    return HttpResponse('''<script>alert('Screen Updated');window.location='/myapp/theatre_view_screen/'</script>''')


def add_time_shedule(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie.objects.all()
    var2=Screen.objects.filter(THEATRE__LOGIN=request.session['lid'])
    return render(request,'theatre/add_time_shedule.html',{'data':var,'data2':var2})

def add_time_shedule_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')



    movie=request.POST['movie']
    screen=request.POST['screen']
    date=request.POST['date']
    from_time=request.POST['from_time']
    to_time=request.POST['to_time']

    var=Shedule()
    var.MOVIE_id=movie
    var.SCREEN_id=screen
    var.date=date
    var.from_time=from_time
    var.to_time=to_time
    var.save()

    return HttpResponse('''<script>alert('Shedule Addedd');window.location='/myapp/add_time_shedule/'</script>''')

def view_shedule(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Shedule.objects.filter(SCREEN__THEATRE__LOGIN=request.session['lid'])

    return render(request,'theatre/view_shedule.html',{'data':var})

def view_shedule_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    f = request.POST['FROMDATE']
    t = request.POST['to']
    var = Shedule.objects.filter(date__range=[f,t])
    return render(request,'theatre/view_shedule.html',{'data':var})

def delete_shedule(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Shedule.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('Shedule Deleted');window.location='/myapp/view_shedule/'</script>''')


def edit_time_shedule(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var3=Shedule.objects.get(id=id)
    var = Movie.objects.all()
    var2 = Screen.objects.filter(THEATRE__LOGIN=request.session['lid'])
    return render(request,'theatre/edit_time_shedule.html',{'data':var3,'movie':var,'screen':var2})


def edit_time_shedule_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    id = request.POST['id']
    movie = request.POST['movie']
    screen = request.POST['screen']
    date = request.POST['date']
    from_time = request.POST['from_time']
    to_time = request.POST['to_time']

    var = Shedule.objects.get(id=id)
    var.MOVIE_id = movie
    var.SCREEN_id = screen
    var.date = date
    var.from_time = from_time
    var.to_time = to_time
    var.save()

    return HttpResponse('''<script>alert('Shedule Updated');window.location='/myapp/view_shedule/'</script>''')

def theatre_review(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theatre_review.objects.filter(THEATRE__LOGIN_id=request.session['lid'])
    return render(request,'theatre/view_review_theatre.html',{'data':var})

def theatre_review_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Theatre_review.objects.filter(date__range=[fromdate, to])
    return render(request,'theatre/view_review_theatre.html',{'data':var})


def theatre_Movie_review(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Movie_review.objects.all()
    return render(request,'theatre/view_review_movie.html',{'data':var})


def theatre_Movie_review_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Movie_review.objects.filter(date__range=[fromdate, to])
    return render(request,'theatre/view_review_movie.html',{'data':var})

def view_user_booking(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Booking.objects.filter(SHEDULE__SCREEN__THEATRE__LOGIN__id=request.session['lid'])
    return render(request,'theatre/view_user_booking.html',{'data':var})


def view_user_booking_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Booking.objects.filter(date__range=[fromdate, to])
    return render(request,'theatre/view_user_booking.html',{'data':var})



def theatre_change_password(request):


    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'theatre/theatre_change_password.html')


def theatre_change_password_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/theatre_change_password/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/theatre_change_password/'</script>''')



def add_promotion(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'theatre/add_Promotion.html')

def add_promotion_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    type=request.POST['movie']
    promotion=request.POST['promotion']
    filename=request.FILES['filename']
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
    fs=FileSystemStorage()
    fs.save(date,filename)
    path=fs.url(date)

    var=Theate_promotion()
    var.THEATRE=Theatre.objects.get(LOGIN_id=request.session['lid'])
    var.type=type
    var.promotion=promotion
    var.date=datetime.now().today().date()
    var.filename=path
    var.save()
    return HttpResponse('''<script>alert('Added');window.location='/myapp/add_promotion/'</script>''')

def view_promotion(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theate_promotion.objects.filter(THEATRE__LOGIN_id=request.session['lid'])
    return render(request,'theatre/view__promotion.html',{'data':var})


def view_promotion_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromdate = request.POST['from']
    to = request.POST['to']
    var = Theate_promotion.objects.filter(date__range=[fromdate, to],THEATRE__LOGIN_id=request.session['lid'])
    return render(request,'theatre/view__promotion.html',{'data':var})


def edit_promotion(request,id):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Theate_promotion.objects.get(id=id)
    return render(request,'theatre/edit_Promotion.html',{'data':var})


def edit_promotion_post(request):

    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    id = request.POST['id']
    type = request.POST['movie']
    promotion = request.POST['promotion']



    var = Theate_promotion.objects.get(id=id)
    var.THEATRE = Theatre.objects.get(LOGIN_id=request.session['lid'])
    var.type = type
    var.promotion = promotion
    var.date = datetime.now().today().date()

    if 'filename' in request.FILES:
        filename = request.FILES['filename']
        if filename.name!='':
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, filename)
            path = fs.url(date)
            var.filename = path
    var.save()

    return HttpResponse('''<script>alert('Updated');window.location='/myapp/view_promotion/'</script>''')



def delete_promotion(request,id):
    var=Theate_promotion.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('Promotion Deleted');window.location='/myapp/view_promotion/'</script>''')







# users flutter

def login2(request):
    a = request.POST['uname']
    b = request.POST['psw']
    result = Login.objects.filter(username=a, password=b)
    if result.exists():
        result2 = Login.objects.get(username=a, password=b)
        if result2.type == 'normal':
            lid=result2.id
            usr=User.objects.get(LOGIN_id=lid)
            return JsonResponse({'status':"ok",'lid':str(lid),'type':'normal','photo':usr.image,'name':usr.name})
        elif result2.type=='premium':
            lid = result2.id
            usr = User.objects.get(LOGIN_id=lid)
            return JsonResponse({'status':"ok",'lid':str(lid),'type':'premium','photo':usr.image,'name':usr.name})



        else:
            return JsonResponse({'status': 'not Ok'})
    else:
        return JsonResponse({'status': 'not Ok'})


def user_post(request):

    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    type=request.POST['type']
    gender=request.POST['gender']
    password=request.POST['password']
    conf=request.POST['confirm']

    if password==conf:
        image = request.POST['image']
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        open(r'C:\Users\GAYATHRI\Desktop\projects\Film_Sportlight\media\user\\' + date1, 'wb').write(fs1)

        path1 = "/media/user/" + date1

        var = Login()
        var.username = email
        var.password = password


        var.type = type
        var.save()

        result = User()
        result.LOGIN = var
        result.name = name
        result.email = email
        result.type=type
        result.gender = gender
        result.phone = phone

        result.image=path1
        result.save()
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "Not Ok"})


def edit_userprofile(request):
    lid = request.POST['loginid']
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    gender = request.POST['gender']
    image = request.POST['image']

    result = User.objects.get(LOGIN_id=lid)
    result.name = name
    result.email = email

    result.gender = gender

    if len(image) > 1:
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        open(r'C:\Users\GAYATHRI\Desktop\projects\Film_Sportlight\media\user\\' + date1, 'wb').write(fs1)
        path1 = "/media/user/" + date1
        result.image = path1

    result.save()
    return JsonResponse({'status': "ok"})


def user_profile(request):

    lid=request.POST['lid']
    var=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': "ok",'name':var.name,'email':var.email,'phone':var.phone,'gender':var.gender,'image':var.image,'type':var.type})



def user_complaint_post(request):
    var=request.POST['comp']
    lid=request.POST['lid']
    date=datetime.now().date().today()

    c_obj=Complaint()
    c_obj.complaint=var
    c_obj.date=date
    uid=User.objects.get(LOGIN_id=lid)
    c_obj.USER=uid
    c_obj.save()

    return JsonResponse({'status': "ok"})


def user_view_complaints(request):
    var=request.POST['lid']
    var2=User.objects.get(LOGIN=var)
    result=Complaint.objects.filter(USER=var2)
    l =[]
    for i in result:
        l.append({'id':i.id, 'complaint':i.complaint,'date':i.date,'reply':i.reply,'status':i.status})
    return JsonResponse({'status': "ok", 'data':l})




def user_view_movie(request):
    user_id=request.POST['lid']
    var=Movie.objects.all()
    l=[]
    for i in var:
        vote='no'
        # if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id).exists():
        #     if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Upvote').exists():
        #         vote=Voting.objects.get(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Upvote').type
        #     if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Downvote').exists():
        #         vote=Voting.objects.get(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Downvote').type
        l.append({'id':i.id, 'name':i.name,'duration':i.duration,'language':i.language,'trailer':i.trailer,'poster':i.poster,'certificate':i.certificate,'cast_and_crew':i.cast_and_crew,'production_house_name':i.production_house_name,'producer_name':i.producer_name,'director_name':i.director_name,'gentre':i.gentre,'vote':vote})
    print(l)
    return JsonResponse({'status':'ok','data':l})




def user_view_promotion(request):
    var=Theate_promotion.objects.all()
    l = []
    for i in var:
        l.append({'id':i.id,'Theatrename':i.THEATRE.name,'type':i.type,'promotion':i.promotion,'date':i.date,'filename':i.filename})
    print(l)
    return JsonResponse({'status':'ok','data':l})


def user_changepassword(request):
    lid = request.POST['lid']
    old = request.POST['old']
    newpass = request.POST['new']
    confirm = request.POST['confirm']

    var = Login.objects.filter(id=lid, password=old)
    if var.exists():
        if newpass == confirm:
            var2 = Login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'Not ok'})
    else:
        return JsonResponse({'status': 'NoT Ok'})



def user_view_theatre(request):
    var=Theatre.objects.all()
    l=[]
    for i in var:


        l.append({'id':i.id,'name':i.name,'place':i.place,'pin':i.pin,'city':i.city,'established':i.established,'phone':i.phone,'email':i.email,'working_time':i.working_time,'about':i.about,'photo':i.photo})
    return JsonResponse({'status':'ok','data':l})



def view_movie_shedule(request):
    var=Shedule.objects.all()
    l=[]
    for i in var:
        l.append({'id': i.id,'movie':i.MOVIE.name,'screen':i.SCREEN.screen_number,'date':i.date,'from_time':i.from_time,'to_time':i.to_time})

    return JsonResponse({'status':'ok','data':l})


def shedule_booking(request):

    return JsonResponse({'status':'ok'})



def user_movie_review(request):
  return JsonResponse({'status': "ok"})

def sent_theatre_review(request):

  return JsonResponse({'status': "ok"})



def user_view_movie_review(request):
    movie=request.POST['movie_id']
    var=Movie_review.objects.filter(MOVIE_id=movie)

    l = []
    for i in var:
        l.append({'id': i.id,'USER':i.USER.name,'MOVIE':i.MOVIE.name,'review':i.review,'date':i.date,})



    return JsonResponse({'status': "ok",'data':l})




def user_view_theate_review(request):
    var=Theatre_review.objects.all()

    l = []
    for i in var:
        l.append({'id': i.id, 'USER': i.USER.name, 'THEATRE': i.THEATRE.name, 'review': i.review, 'date': i.date, })

    return JsonResponse({'status': "ok"})


def sent_theatre_review1(request):
    lid=request.POST['lid']
    review=request.POST['review']
    theatre=request.POST['theatre_id']

    date=datetime.now().date().today()
    var=Theatre_review()
    var.USER=User.objects.get(LOGIN_id=lid)
    var.review=review
    var.date=date
    var.THEATRE_id=theatre
    var.save()

    return JsonResponse({'status': "ok"})

def sent_movie_review(request):
    lid=request.POST['lid']
    review=request.POST['review']
    movie=request.POST['movie_id']
    date=datetime.now().date().today()
    a=Movie_review()
    a.date=date
    a.MOVIE_id=movie
    a.USER=User.objects.get(LOGIN_id=lid)
    a.review=review
    a.save()



    return JsonResponse({'status': "ok"})



def shedeule_booking(request):
    lid = request.POST['lid']
    total_seat = request.POST['total_seat']
    shedule = request.POST['shedule_id']
    prebook = request.POST['prebook']
    date=datetime.now().date().today()
    var=Booking()
    var.USER=User.objects.get(LOGIN_id=lid)
    var.total_seat=total_seat
    var.SHEDULE_id=shedule
    var.date=date
    var.prebook=prebook
    var.save()
    return JsonResponse({'status':'ok'})


def  view_booking_user(request):
    var = request.POST['lid']
    var2 = User.objects.get(LOGIN=var)
    result = Booking.objects.filter(USER=var2)
    l = []
    for i in result:
        pbook='Normal'
        if i.prebook=='yes':
            pbook='Premium'
        l.append({'id': i.id, 'SHEDULE': i.SHEDULE.MOVIE.name, 'USER': i.USER.name, 'total_seat': i.total_seat,'movie_name':i.SHEDULE.MOVIE.name,'moviedate':i.SHEDULE.date,'date':i.date,'from_time':i.SHEDULE.from_time,'to_time':i.SHEDULE.to_time,'prebook':pbook})

    return JsonResponse({'status':'ok','data':l})

def premium_shedeule_booking(request):
    lid = request.POST['lid']
    total_seat = request.POST['total_seat']
    shedule = request.POST['shedule_id']
    date=datetime.now().date().today()
    var=Booking()
    var.USER=User.objects.get(LOGIN_id=lid)
    var.total_seat=total_seat
    var.SHEDULE_id=shedule
    var.date=date
    var.prebook='prebook'
    var.save()
    return JsonResponse({'status':'ok'})



def view_prebook(request):
    var=Booking.objects.filter(prebook='yes')
    l=[]
    for i in var:
        l.append({'id': i.id, 'total_seat': i.total_seat, 'date': i.date, 'SHEDULE': i.SHEDULE.MOVIE.name,'shedule_date':i.SHEDULE.date,

                  'from_time': i.SHEDULE.from_time, 'to_time': i.SHEDULE.to_time})

    return JsonResponse({'status': 'ok', 'data': l})


def upvote(request):
    question=request.POST['question_id']
    lid=request.POST['lid']

    Voting.objects.filter(USER__LOGIN_id=lid, QUESTION_id=question).delete()
    var=Voting()
    var.QUESTION_id=question
    var.USER=User.objects.get(LOGIN_id=lid)
    var.type='Upvote'
    var.save()

    return JsonResponse({'status': 'ok', })


def downvote(request):
    question=request.POST['question_id']
    lid=request.POST['lid']

    Voting.objects.filter(USER__LOGIN_id=lid, QUESTION_id=question).delete()
    var=Voting()
    var.QUESTION_id=question
    var.USER=User.objects.get(LOGIN_id=lid)
    var.type='Downvote'
    var.save()


    return JsonResponse({'status': 'ok', })



def sent_question(request):
    lid=request.POST['lid']
    movie=request.POST['movie_id']
    question=request.POST['question']
    date=datetime.now().date().today()

    var=Question()
    var.date=date
    var.question=question
    var.MOVIE_id=movie
    var.USER=User.objects.get(LOGIN_id=lid)
    var.status='Pending'
    var.answer='pending'
    var.save()

    return JsonResponse({'status':'ok'})


# def user_view_movie(request):
#     user_id=request.POST['lid']
#     var=Movie.objects.all()
#     l=[]
#     for i in var:
#         vote='no'
#         if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id).exists():
#             if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Upvote').exists():
#                 vote=Voting.objects.get(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Upvote').type
#             if Voting.objects.filter(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Downvote').exists():
#                 vote=Voting.objects.get(USER__LOGIN_id=user_id, MOVIE_id=i.id, type='Downvote').type
#         l.append({'id':i.id, 'name':i.name,'duration':i.duration,'language':i.language,'trailer':i.trailer,'poster':i.poster,'certificate':i.certificate,'cast_and_crew':i.cast_and_crew,'production_house_name':i.production_house_name,'producer_name':i.producer_name,'director_name':i.director_name,'gentre':i.gentre,'vote':vote})
#     print(l)
#     return JsonResponse({'status':'ok','data':l})



def user_view_movie_questions(request):
    user_id=request.POST['lid']

    movie=request.POST['movie_id']
    var=Question.objects.filter(MOVIE_id=movie)

    l = []
    for i in var:

        vote = 'no'
        ucnt = 0
        dcnt = 0
        if Voting.objects.filter(USER__LOGIN_id=user_id, QUESTION_id=i.id).exists():
            if Voting.objects.filter(USER__LOGIN_id=user_id, QUESTION_id=i.id, type='Upvote').exists():
                vote = Voting.objects.get(USER__LOGIN_id=user_id, QUESTION_id=i.id, type='Upvote').type
                ucnt+=1
            if Voting.objects.filter(USER__LOGIN_id=user_id, QUESTION_id=i.id, type='Downvote').exists():
                vote = Voting.objects.get(USER__LOGIN_id=user_id, QUESTION_id=i.id, type='Downvote').type
                dcnt += 1
        l.append({'id': i.id,'USER':i.USER.name,'MOVIE':i.MOVIE.name,'status':i.status,'date':i.date,'question':i.question,'answer':i.answer, 'vote':vote, 'unct':str(ucnt), 'dnct':str(dcnt)})

    print(l)

    return JsonResponse({'status': "ok",'data':l})