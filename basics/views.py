from django.shortcuts import render, HttpResponse, redirect
from pathlib import Path
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserDetails  # Ensure correct import

# Create your views here

def About(request):
    return render(request, 'About.html')

def Project(request):
    return render(request, 'Project.html')

def Predict(request):
    if request.method == "POST":
        data = request.POST
        if 'buttonpredict' in request.POST:
            try:
                dia = float(data.get('textdia'))
                hei_left = float(data.get('textheileft'))
                hei_rig = float(data.get('textheirig'))
                mar_low = float(data.get('textmarlow'))
                mar_up = float(data.get('textmarup'))
                leng = float(data.get('textleng'))
            except (TypeError, ValueError):
                return render(request, 'Predict.html', context={'res': 'Please enter valid numeric values for all six fields.'})

            import pandas as pd
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.preprocessing import LabelEncoder

            # Place the original training file at the project root, or set FAKE_BILLS_DATASET.
            dataset_path = Path(os.environ.get('FAKE_BILLS_DATASET', settings.BASE_DIR / 'fake_bills.csv'))
            if not dataset_path.is_file():
                return render(request, 'Predict.html', context={
                    'res': 'Training dataset not found. Add fake_bills.csv to the project root or set FAKE_BILLS_DATASET to its path. Manual inputs are the bill features; the classifier still needs labelled training data.'
                })

            training_data = pd.read_csv(dataset_path)
            required_columns = ['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length', 'is_genuine']
            missing = [column for column in required_columns if column not in training_data.columns]
            if missing:
                return render(request, 'Predict.html', context={'res': 'Training CSV is missing required columns: ' + ', '.join(missing)})

            med_val = training_data['margin_low'].median()
            training_data['margin_low'] = training_data['margin_low'].fillna(med_val)
            encoder = LabelEncoder()
            training_data['is_genuine'] = encoder.fit_transform(training_data['is_genuine'].astype(str))
            features = training_data[['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length']]
            labels = training_data['is_genuine']
            model = DecisionTreeClassifier(random_state=42)
            model.fit(features, labels)
            prediction = model.predict([[dia, hei_left, hei_rig, mar_low, mar_up, leng]])
            genuine_label = encoder.transform(['True'])[0] if 'True' in encoder.classes_ else encoder.transform(['Genuine'])[0] if 'Genuine' in encoder.classes_ else 1
            result_text = 'Bill is Genuine' if prediction[0] == genuine_label else 'Bill is Fake'
            return render(request, 'Predict.html', context={'res': result_text})
    return render(request, 'Predict.html')

def homepage(request):
    return render(request, 'homepage.html')

def base(request):
    return render(request, 'base.html')

def signuppage(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        pass1 = data.get('password1')
        pass2 = data.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")

        if UserDetails.objects.filter(username=username).exists():
            return HttpResponse("Username already taken!")
        if UserDetails.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")

        user = UserDetails(username=username, email=email, phone_number=phone, address=address)
        user.save()
        return HttpResponse("User registered successfully!")

    return render(request, 'signuppage.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'loginpage.html')

def logout_view(request):
    logout(request)
    return redirect('loginpage')

# models.py file
from django.db import models

class UserDetails(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.username