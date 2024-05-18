from django.shortcuts import render, redirect
from .models import User, Team, Idea
from django.contrib import messages
import bcrypt


def registration(request):
    user_id = request.session.get("user_id")

    if user_id:
        return redirect("app1:ideas")

    return render(request, "registration.html")


def register(request):
    if request.method == "POST":

        errors = User.objects.validate(request.POST)

        # There is some errors
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("app1:registration")

        first_name_form = request.POST["first_name"]
        last_name_form = request.POST["last_name"]
        email_form = request.POST["email"]
        password_form = request.POST["password1"]
        confirm_password_form = request.POST["password2"]

        if password_form == confirm_password_form:
            hash_password = bcrypt.hashpw(
                password_form.encode(), bcrypt.gensalt()
            ).decode()

            new_user = User.objects.create(
                first_name=first_name_form,
                last_name=last_name_form,
                email=email_form,
                password=hash_password,
            )

            request.session["user_id"] = new_user.id
            request.session["first_name"] = new_user.first_name

            return redirect("app1:ideas")

        # if password didn't match
        else:
            messages.error(request, "Password not match.")
            return redirect("app1:registration")


def login(request):
    if request.method == "POST":
        email_form = request.POST["email"]
        password_form = request.POST["password1"]

        users = User.objects.filter(email=email_form)

        if len(users) == 0:
            messages.error(request, "Email doesn't exist.")
            return redirect("app1:registration")

        if bcrypt.checkpw(password_form.encode(), users.first().password.encode()):
            request.session["user_id"] = users[0].id
            request.session["first_name"] = users[0].first_name

            return redirect("app1:ideas")
        # if password is wrong
        else:
            messages.error(request, "Password not correct.")
            return redirect("app1:registration")


def logout(request):
    request.session.flush()
    return redirect("app1:registration")


def ideas(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    context = {"ideas": Idea.objects.all()}
    return render(request, "ideas.html", context)


def team(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    context = {"teams": Team.objects.all()}
    return render(request, "team.html", context)


def add_idea(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    errors = Idea.objects.validate(request.POST)

    if len(errors) > 0:
        for error in errors.values():
            messages.error(request, error)
        return redirect("app1:ideas")

    user = User.objects.get(id=user_id)

    if not user.team:
        messages.error(request, "User Should Join a team first")
        return redirect("app1:ideas")

    idea_text = request.POST["idea_text"]

    Idea.objects.create(text=idea_text, user=user)

    return redirect("app1:ideas")


def create_team(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    user = User.objects.get(id=user_id)

    if user.team:
        messages.error(request, "User already on a team")
        return redirect("app1:team")

    team_name = request.POST["team_name"]
    team = Team.objects.create(name=team_name)

    user.team = team
    user.save()

    return redirect("app1:ideas")


def join_team(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    user = User.objects.get(id=user_id)

    if user.team:
        messages.error(request, "User already on a team")
        return redirect("app1:team")

    team_id = request.POST["team_id"]
    team = Team.objects.get(id=team_id)
    user.team = team
    user.save()

    return redirect("app1:ideas")


def delete_idea(request, pk):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    idea = Idea.objects.get(id=pk)
    idea.delete()
    return redirect("app1:ideas")


def user_ideas(request, pk):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("app1:registration")

    user = User.objects.get(id=pk)

    ideas = Idea.objects.filter(user=user)

    context = {"ideas": ideas, "user": user}

    return render(request, "user_idea.html", context)


def edit_idea(request, pk):

    if request.method == "POST":
        print("editing")
        errors = Idea.objects.validate(request.POST)

        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("app1:edit_idea", pk=pk)

        idea_id = request.POST["idea_id"]
        idea = Idea.objects.get(id=idea_id)
        idea.text = request.POST["idea_text"]
        idea.save()

        return redirect("app1:ideas")

    idea = Idea.objects.get(id=pk)
    context = {"idea": idea}
    return render(request, "edit.html", context)
