from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    image=models.CharField(max_length=300)
    type=models.CharField(max_length=300)

    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)



class Movie(models.Model):
    name=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    trailer=models.CharField(max_length=800)
    poster=models.CharField(max_length=500)
    certificate=models.CharField(max_length=100)
    cast_and_crew=models.CharField(max_length=300)
    production_house_name=models.CharField(max_length=100)
    producer_name=models.CharField(max_length=100)
    director_name=models.CharField(max_length=100)
    gentre=models.CharField(max_length=100)


class Theatre(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    city=models.CharField(max_length=800)
    ownername=models.CharField(max_length=500)
    phone=models.CharField(max_length=100)
    photo=models.CharField(max_length=300)
    established=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    working_time=models.CharField(max_length=100)
    about=models.CharField(max_length=500)
    status=models.CharField(max_length=500)
    password=models.CharField(max_length=100)


class Screen(models.Model):
    THEATRE=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    size=models.CharField(max_length=100)
    screen_number=models.CharField(max_length=100)
    audio_type=models.CharField(max_length=100)
    audio_quality=models.CharField(max_length=800)
    seat_charge=models.CharField(max_length=500)
    total_set=models.CharField(max_length=100)


class Shedule(models.Model):
    MOVIE = models.ForeignKey(Movie, on_delete=models.CASCADE)
    SCREEN = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100)

class Booking(models.Model):
    SHEDULE = models.ForeignKey(Shedule, on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    total_seat = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    prebook = models.CharField(max_length=100)

class Theate_promotion(models.Model):

    THEATRE=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    # SHEDULE=models.ForeignKey(Shedule,on_delete=models.CASCADE)
    type=models.CharField(max_length=100)
    promotion=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    filename=models.CharField(max_length=500)


class Theatre_review(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    THEATRE=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    date=models.CharField(max_length=100)

class Movie_review(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    MOVIE=models.ForeignKey(Movie,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    date=models.CharField(max_length=100)



class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)

    date=models.CharField(max_length=100)
    complaint=models.CharField(max_length=300)
    status = models.CharField(max_length=100, default='pending')
    reply = models.CharField(max_length=100, default='pending')

class Question(models.Model):
    MOVIE = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.CharField(max_length=100, default='1')
    status = models.CharField(max_length=100, default='1')
    question = models.CharField(max_length=500, default='1')
    answer = models.CharField(max_length=500, default='1')


class Voting(models.Model):
    QUESTION=models.ForeignKey(Question,on_delete=models.CASCADE,default=1)
    USER=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    type = models.CharField(max_length=100, default='1')




