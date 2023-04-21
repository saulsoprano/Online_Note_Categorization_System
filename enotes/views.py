from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, logout, login

import pickle


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def register(request):
    error = ""
    if request.method == 'POST':
        fn = request.POST['firstName']
        ln = request.POST['lastName']
        e = request.POST['email']
        p = request.POST['password']
        c = request.POST['ContactNo']
        ab = request.POST['About']
        role = "ROLE_USER"

        try:
            user = User.objects.create_user(username=e, password=p, first_name=fn, last_name=ln)
            Signup.objects.create(user=user, ContactNo=c, About=ab, Role=role)
            error = "no"
        except:
            error = "yes"
    return render(request, 'register.html', locals())


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'user_login.html', locals())


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)
    important = request.GET.get('important', False)
    totalcategory = Category.objects.filter(signup=signup).count()
    totalnotes = Notes.objects.filter(signup=signup).count()

    if important:
        notes = Notes.objects.filter(signup=signup, is_important=True)
    else:
        notes = Notes.objects.filter(signup=signup)

    return render(request, 'dashboard.html', locals())


def profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)

    if request.method == "POST":

        fname = request.POST['firstName']
        lname = request.POST['lastName']
        contactNo = request.POST['ContactNo']
        about = request.POST['About']

        signup.user.first_name = fname
        signup.user.last_name = lname
        signup.ContactNo = contactNo
        signup.About = about

        try:
            signup.save()
            signup.user.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'profile.html', locals())


def manageCategory(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)
    category = Category.objects.filter(signup=signup)

    if request.method == "POST":
        categoryName = request.POST['categoryName']
        try:
            Category.objects.create(signup=signup, categoryName=categoryName)
            error = "no"
        except:
            error = "yes"
    return render(request, 'manageCategory.html', locals())


def editCategory(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    category = Category.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        categoryName = request.POST['categoryName']

        category.categoryName = categoryName

        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'editCategory.html', locals())


def deleteCategory(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manageCategory')


def manageNotes(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)
    category = Category.objects.filter(signup=signup)

    notes = Notes.objects.filter(Q(category__in=category)).order_by('-CreationDate')

    if request.method == "POST":
        cid = request.POST['category']
        categoryid = Category.objects.get(id=cid)
        noteDescription = request.POST['noteDescription']
        is_important = request.POST.get('important', False) == 'on'

        with open('model_final.pkl', 'rb') as f:
            saved_data = pickle.load(f)
        model = saved_data['model']
        categories = saved_data['categories']
        prediction = model.predict([noteDescription])
        predicted_category = categories[prediction[0]]
        separated_words = predicted_category.split('.')
        formatted_category = ' '.join(['#' + word for word in separated_words])
        tag = formatted_category.replace(' #', '  #', 1)
        # slug = slugify(predicted_category)[:50]  # generate a slug from the predicted tag
        # tag = '#' + predicted_category

        try:
            Notes.objects.create(signup=signup, category=categoryid, noteDescription=noteDescription,
                                 is_important=is_important, tags=tag)
            error = "no"
        except:
            error = "yes"
    return render(request, 'manageNotes.html', locals())



def editNotes(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    notes = Notes.objects.get(id=pid)
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)
    category = Category.objects.filter(signup=signup)
    is_important = request.POST.get('important') == 'on'

    if request.method == "POST":
        cid = request.POST['category']
        categoryid = Category.objects.get(id=cid)
        noteDescription = request.POST['noteDescription']

        notes.category = categoryid
        notes.noteDescription = noteDescription
        notes.is_important = is_important
        try:
            notes.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'editNotes.html', locals())


def viewNotes(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    notes = Notes.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)
    noteshistory = Noteshistory.objects.filter(signup=signup)

    if request.method == "POST":
        noteDetails = request.POST['noteDetails']

        try:
            Noteshistory.objects.create(note=notes, signup=signup, noteDetails=noteDetails)
            error = "no"
        except:
            error = "yes"
    return render(request, 'viewNotes.html', locals())


def deleteNotesHistory(request, pid):
    noteshistory = Noteshistory.objects.get(id=pid)
    noteshistory.delete()
    return redirect('manageNotes')


def deleteNotes(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect('manageNotes')


def generalCategory(request):
    return render(request, 'generalCategory.html')


def specificCategory(request):
    return render(request, 'specificCategory.html')


def resultSpecific(request):
    if request.method == 'POST':
        # load the saved model and categories
        with open('model_final.pkl', 'rb') as f:
            saved_data = pickle.load(f)
        model = saved_data['model']
        categories = saved_data['categories']

        # get the input data from the form
        input_data = request.POST['Content']

        # make a prediction using the loaded model
        prediction = model.predict([input_data])

        # render the results on the website
        predicted_category = categories[prediction[0]]
        return render(request, 'resultSpecific.html', {'prediction': predicted_category})

    return render(request, 'specificCategory.html')


def resultGeneral(request):
    categories = ['Religion',
                  'Technology',
                  'Technology',
                  'Technology',
                  'Technology',
                  'Technology',
                  'Miscellaneous',
                  'Miscellaneous',
                  'Miscellaneous',
                  'Sports',
                  'Sports',
                  'Science',
                  'Science',
                  'Medicine',
                  'Space',
                  'Religion',
                  'Politics',
                  'Politics',
                  'Politics',
                  'Religion']

    if request.method == 'POST':
        # load the saved model
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        # get the input data from the form
        input_data = request.POST['Content']
        # make a prediction using the loaded model
        prediction = model.predict([input_data])
        # render the results on the website
        return render(request, 'resultGeneral.html', {'prediction': categories[prediction[0]]})
    return render(request, 'generalCategory.html')


def searchNotes(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)

    sd = None
    if request.method == 'POST':
        sd = request.POST['search']
    try:
        notes = Notes.objects.filter(Q(category__categoryName__icontains=sd))
    except:
        notes = ""
    return render(request, 'searchNotes.html', locals())


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'changePassword.html', locals())


def Logout(request):
    logout(request)
    return redirect('index')
