# Time-stamp: <2018-03-17 14:33:33 rene>
#
# Copyright (C) 2017 Rene Maurer
# This file is part of tangodjsforgoodsound.
#
# tangodjsforgoodsound is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# tangodjsforgoodsound is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------

import os

from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from forms import ContactForm, RegisterForm, DJEditForm, SubscriberPasswordForm
from .models import DJ
from .common import createDJContext, sendContactEmail, sendRegistrationEmail, \
    sendRegistrationDeletedEmail

SHOW_MAINTENANCE_PAGE = ".qmail-maintenance"


def debug(s):
    if 1:
        print ">>>>", s


@login_required
def change_password(request):
    if request.method == "POST":
        form = SubscriberPasswordForm(request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data["new_password1"])
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important!
                debug("Password for user %s set" % request.user)
            except Exception:
                # This should not happen
                print ">>>>>>>> Unexcpected error in change_password()"
                context = {"form": form}
                context = createDJContext(request, DJ, context)
                return render(request, "change_password.html", context)
            else:
                context = {"form": form}
                context = createDJContext(request, DJ, context)
                return render(request, "change_password_success.html", context)
    else:
        form = SubscriberPasswordForm()
    context = {"form": form}
    context = createDJContext(request, DJ, context)
    return render(request, "change_password.html", context)


def copyright(request):
    context = createDJContext(request, DJ)
    return render(request, "copyright.html", context)


def linkpage(request):
    context = createDJContext(request, DJ)
    return render(request, "linkpage.html", context)


def index(request):
    home = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home, SHOW_MAINTENANCE_PAGE)):
        orderBy = ["country", "namesort"]
        djL = DJ.objects.order_by(*orderBy).filter(number_of_milongas__gte=1)
        context = {"djList": djL}
        context = createDJContext(request, DJ, context)
        return render(request, "index.html", context)
    return render(request, "index_empty.html")


def contact(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        firstname = request.POST.get("contact_firstname", '')
        lastname = request.POST.get("contact_lastname", '')
        email = request.POST.get("contact_email", '')
        content = request.POST.get("contact_content", '')
        magic = request.POST.get("contact_magic", '')
        if form.is_valid():
            email = sendContactEmail(firstname, lastname, email, content,
                                     magic)
            context = createDJContext(request, DJ)
            return redirect("contactfeedback")
        context = {"form": form}
        return render(request, "contact.html", context)
    context = {"form": form_class}
    context = createDJContext(request, DJ, context)
    return render(request, "contact.html", context)


def contactfeedback(request):
    context = createDJContext(request, DJ)
    return render(request, "contactfeedback.html", context)


def mission(request):
    context = createDJContext(request, DJ)
    return render(request, "mission.html", context)


def more(request):
    context = createDJContext(request, DJ)
    return render(request, "more.html", context)


def loginredirect(request):
    if request.user.is_authenticated():
        user = request.user
        if user.id == 1:
            return redirect("/admin")
        else:
            dj = DJ.objects.get(user=user)
            if dj:
                return djdetail(request, dj.id)
    # This should not happen
    return index(request)


def customlogout(request):
    model_changed = False
    if not model_changed:
        logout(request)
        return index(request)


def djdetail(request, dj_id):
    dj = get_object_or_404(DJ, pk=dj_id)
    return render(request, "djdetail.html", {"dj": dj})


def djedit(request):
    if request.user.is_authenticated():
        debug("djedit called")
        html = "djedit.html"
        user = request.user
        djobject = DJ.objects.get(user=user)
        debug("djedit %s selected" % djobject)
        if request.method == 'POST':
            debug("djedit POST")
            djform = DJEditForm(request.POST, instance=djobject)
            djform.set_namesort(request)
            djform.request = request
            if djform.is_valid():
                debug("djedit form valid")
                try:
                    theUser = User.objects.all().filter(id=user.id)[0]
                except Exception:
                    theUser = None
                if theUser:
                    debug("djedit user found")
                    loginAddress = djform.cleaned_data.get("useremail")
                    debug("djedit => save()")
                    djform.save()
                    if not loginAddress == theUser.username \
                       or not loginAddress == theUser.email:
                        debug("New Username %s => %s" % (theUser.username,
                                                         loginAddress))
                        debug("New Useremail %s => %s" % (theUser.email,
                                                          loginAddress))
                        debug("auth_user => save()")
                        theUser.username = loginAddress
                        theUser.email = loginAddress
                        User.save(theUser)
                        # save user
                    html = "djdetail.html"
                else:
                    debug("djedit user not found")
            else:
                debug("djedit form not valid")
        else:
            debug("djedit GET")
            djform = DJEditForm(instance=djobject)

        context = {"form": djform, "user": user}
        context = createDJContext(request, DJ, context)
        return render(request, html, context)

    # This should not happen!
    return index(request)


def djdelete(request):
    if request.user.is_authenticated():
        debug("djdelete called")
        user = request.user
        djobject = DJ.objects.get(user=user)
        debug("djdelete djobject = %s" % djobject)
        try:
            theUser = User.objects.all().filter(id=user.id)[0]
        except Exception:
            theUser = None
        try:
            theDJ = DJ.objects.all().filter(user=user)[0]
        except Exception:
            theDJ = None
        debug("djdelete, DJ = %d %s" % (theDJ.id, theDJ))
        debug("djdelete, user = %d %s" % (theUser.id, theUser))
        if request.method == "POST" and theUser and theDJ:
            logout(request)
            debug("logged out user")
            theDJ.delete()
            debug("DJ deleted")
            theUser.delete()
            debug("User deleted")
            sendRegistrationDeletedEmail(theUser.first_name, theUser.last_name,
                                         theDJ.name, theUser.email)
            return render(request, "djdeleted.html")
        context = {"user": user}
        context = createDJContext(request, DJ, context)
        return render(request, "djdelete.html", context)
    return index(request)


def djdeleted(request):
    return render(request, "djdeleted.html")


def register(request):
    form_class = RegisterForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        firstname = request.POST.get("register_firstname", '')
        lastname = request.POST.get("register_lastname", '')
        djname = request.POST.get("register_djname", '')
        email = request.POST.get("register_email", '')
        password1 = request.POST.get("register_password1", '')
        # password2
        magic = request.POST.get("register_magic", '')
        if form.is_valid():
            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=email,
                email=email,
                password=password1)
            dj = DJ(user=user,
                    useremail=email,
                    name=djname,
                    number_of_milongas=0)
            dj.save()
            content = ""
            email = sendRegistrationEmail(firstname, lastname, djname, email,
                                          content, magic)
            return redirect("registered")
        return render(request, "registration/register.html", {"form": form, })
    return render(request, "registration/register.html",
                  {"form": form_class, })


def registered(request):
    return render(request, "registration/registered.html")
