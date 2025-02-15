from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from hiro_backend.database import (
    create_account,
    find_account,
    create_session_id,
    check_session_id,
    delete_session_id,
)
from HIRO.HIRO import HEALTHCARE_COMPANION

TRAINING_DATA = "DATASET/Training.csv"
TESTING_DATA = "DATASET/Testing.csv"
SYMPTOM_DESCRIPTION = "DATASET/symptom_Description.csv"
PRECAUTION_DATA = "DATASET/precautions.csv"
CHAT_DATASET = "DATASET/intents.json"

hiro = HEALTHCARE_COMPANION(
    TRAINING_DATA, TESTING_DATA, SYMPTOM_DESCRIPTION, PRECAUTION_DATA, CHAT_DATASET
)
hiro.process_training_data(show_models_stats=False)
hiro.build_robust_model()


# Create your views here.
def Homepage(request):
    try:
        user_prompt = request.POST.get("user_prompt")
        if user_prompt != None:
            extracted_symptoms = hiro.extract_symptoms(user_prompt, show_extracted_symptoms=True)
            if extracted_symptoms:
                disease_predicted = hiro.predict_disease_from_symptoms(extracted_symptoms)
                disease_description = hiro.get_description(disease_predicted["Final Prediction"])
                disease_precaution = hiro.get_precautions(disease_predicted["Final Prediction"])

                return render(
                    request,
                    "webapp/index.html",
                    {
                        "user_prompt": user_prompt,
                        "response": "None",
                        "extracted_symptoms": extracted_symptoms,
                        "disease_from_test1": disease_predicted["Random Forest"],
                        "disease_from_test2": disease_predicted["SVC"],
                        "disease_from_test3": disease_predicted["Naive Bayes"],
                        "final_prediction": disease_predicted["Final Prediction"],
                        "disease_description": disease_description,
                        "disease_precaution": disease_precaution,
                    },
                )

            else:
                response = hiro.talk_to_user(user_prompt)
                return render(
                    request,
                    "webapp/index.html",
                    {
                        "user_prompt": user_prompt,
                        "response": response,
                        "extracted_symptoms": "None",
                        "disease_from_test1": "None",
                        "disease_from_test2": "None",
                        "disease_from_test3": "None",
                        "final_prediction": "None",
                        "disease_description": "None",
                        "disease_precaution": "None",
                    },
                )
    except Exception as e:
        print(e)
        return render(
            request,
            "webapp/index.html",
            {
                "user_prompt": user_prompt,
                "response": "None",
                "extracted_symptoms": "None",
                "disease_from_test1": "None",
                "disease_from_test2": "None",
                "disease_from_test3": "None",
                "final_prediction": "None",
                "disease_description": "None",
                "disease_precaution": "None",
            },
        )

    # Authentication
    session_id = request.session.get("session_id")
    if session_id == None:
        return redirect("login")
    if session_id != None:
        account = check_session_id(session_id)
        if account == None:
            return redirect("login")

    return render(request, "webapp/index.html")


def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == None or password == None:
            messages.error(request, "Please fill in all the fields!")
            return render(request, "webapp/login.html")

        account = find_account(email)

        if account == None:
            messages.error(request, "Account not found!")
            return render(request, "webapp/login.html")

        if account["password"] != password:
            messages.error(request, "Incorrect password!")
            return render(request, "webapp/login.html")

        session_id = create_session_id(email, password)
        request.session["session_id"] = session_id

        messages.success(request, "Logged in successfully!")
        return redirect("homepage")

    session_id = request.session.get("session_id")
    if session_id != None:
        account = check_session_id(session_id)
        if account != None:
            return redirect("homepage")

    return render(request, "webapp/login.html")


def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        account = find_account(email)
        if account != None:
            messages.error(request, "Email already in use!")
            return render(request, "webapp/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "webapp/register.html")

        if username != None and email != None and password != None:
            create_account(username, email, password)
            messages.success(request, "Account created successfully!")

    return render(request, "webapp/register.html")


def Logout(request):
    session_id = request.session.get("session_id")
    if session_id != None:
        delete_session_id(session_id)
        del request.session["session_id"]

    return redirect("login")
