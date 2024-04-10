"""from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import EndnodeForm
from django.contrib import messages
from .models import Endnode
from django.contrib.auth.decorators import login_required
import json, requests
from rest_framework.views import APIView


# @login_required(login_url = "user:login")
def EndNodes(request):
    endnodes = Endnode.objects.all()

    context = {
        "endnodes": endnodes
    }

    return render(request, "end_node_index.html", context)


# @login_required(login_url = "user:login")
def AddEndNode(request):

    form = EndnodeForm(request.POST or None)
    if form.is_valid():

        endnode = form.save(commit=False)
        endnode.author = request.user

        activationMethodabp = request.POST.get("abp", False)
        activationMethodotaa = request.POST.get("otaa", False)
        if (activationMethodabp == "abp" and activationMethodotaa == False):
            activationmethod = "ABP"
        if (activationMethodotaa == "otaa" and activationMethodabp == False):
            activationmethod = "OTAA"
        if (activationMethodabp == False and activationMethodotaa == False):
            activationmethod = "ABP"
        endnode.activation_method = activationmethod

        devicetypetemp = request.POST.get("temphum", False)
        devicetypeenergy = request.POST.get("energy", False)
        devicetypewater = request.POST.get("water", False)
        if (devicetypetemp == "temphum" and devicetypeenergy == False and devicetypewater == False):
            devicetype = "Temperature-Humidity"
        if (devicetypeenergy == "energy" and devicetypetemp == False and devicetypewater == False):
            devicetype = "Energy"
        if (devicetypewater == "water" and devicetypetemp == False and devicetypeenergy == False):
            devicetype = "Water"
        endnode.device_type = devicetype

        endnode.status = "Connected"

        createEndnodeResponse = CreateEndnode(endnode.name, endnode.description, endnode.dev_eui)

        if (createEndnodeResponse == "OK"):
            messages.success(request, messages.SUCCESS, "Endnode Added!")
            endnode.save()
        else:
            messages.add_message(request, messages.ERROR, "Progress Error!")

        messages.success(request, "Endnode added successfully")

        return render(request, "end_node_add.html")
    return render(request, "end_node_add.html", {"form": form})


def CreateEndnode(endnodename, endnodedescription, endnodedeveui):

    url = "http://172.16.4.40:8080/api/devices"
    token = GetTokenFromLoraAPI()
    profileID = GetProfileID(token, "3")

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    data = {
        "device": {
            "applicationID": "3",
            "description": str(endnodedescription),
            "devEUI": str(endnodedeveui),
            "deviceProfileID": str(profileID),
            "name": str(endnodename),
            "referenceAltitude": "0"
        }
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    print (response.status_code, response.text)

    if (response.status_code == 200):
        return "OK"
    else:
        return "Error"


def DeleteEndnode(request, id):

    endnode = Endnode.objects.get(id = id)
    endnodeid = endnode.id

    context = {
        "endnode": endnode
    }

    if (request.method == "POST"):
        print("Delete Progress Started!")

        endnodeEui = endnode.dev_eui

        url = "http://172.16.4.40:8080/api/devices/{}".format(endnodeEui)

        token = GetTokenFromLoraAPI()

        headers = {
            "Grpc-Metadata-Authorization": str(token)
        }

        response = requests.delete(url, headers=headers)

        responseInternal = Endnode.objects.get(id=id).delete()

        print (response)
        print (responseInternal)

        return redirect("http://127.0.0.1:8000/endnode/")
    return render(request, "delete_endnode.html", context=context)


def EditEndnode(request, id):

    endnode = Endnode.objects.get(id=id)

    context = {
        "endnode": endnode
    }

    if (request.method == "POST"):

        endnode.author = request.user
        activationMethodabp = request.POST.get("abp", False)
        activationMethodotaa = request.POST.get("otaa", False)
        if (activationMethodabp == "abp" and activationMethodotaa == False):
            activationmethod = "ABP"
        if (activationMethodotaa == "otaa" and activationMethodabp == False):
            activationmethod = "OTAA"
        if (activationMethodabp == False and activationMethodotaa == False):
            activationmethod = "ABP"
        endnode.activation_method = activationmethod
        devicetypetemp = request.POST.get("temphum", False)
        devicetypeenergy = request.POST.get("energy", False)
        devicetypewater = request.POST.get("water", False)
        if (devicetypetemp == "temphum" and devicetypeenergy == False and devicetypewater == False):
            devicetype = "Temperature-Humidity"
        if (devicetypeenergy == "energy" and devicetypetemp == False and devicetypewater == False):
            devicetype = "Energy"
        if (devicetypewater == "water" and devicetypetemp == False and devicetypeenergy == False):
            devicetype = "Water"
        endnode.device_type = devicetype
        endnode.status = "Connected"

        endnode.save()

        updateEndnodeResponse = UpdateEndnode(str(endnode.name), str(endnode.description), str(endnode.dev_eui))

        print (updateEndnodeResponse)

        return redirect("/endnode/")
    return render(request, "edit_endnode.html", context=context)


def UpdateEndnode(endnodename, endnodedescription, endnodedeveui):

    url = "http://172.16.4.40:8080/api/devices/{}".format(endnodedeveui)

    token = GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    data = {
        "device": {
            "applicationID": "3",
            "description": str(endnodedescription),
            "devEUI": str(endnodedeveui),
            "deviceProfileID": str(profileID),
            "name": str(endnodename),
            "referenceAltitude": "0"
        }
    }

    data = json.dumps(data)

    print(data)

    response = requests.put(url, headers=headers, data=data)

    if (response.status_code == 200):
        return "OK"
    else:
        return "Error"


def GetTokenFromLoraAPI():

    url = "http://172.16.4.40:8080/api/internal/login"

    data = '{"password":"admin", "username": "admin"}'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=data)
    responseText = response.text
    token = json.loads(responseText)["jwt"]
    return token


def GetProfileID(token, applicationID):

    url = "http://172.16.4.40:8080/api/device-profiles?limit=1&applicationID={}".format(applicationID)

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers=headers)

    jsonObject = json.loads(response.text)
    profileID = jsonObject["result"][0]["id"]

    return str(profileID)


def GetAllEndnodesFunc(request):

    url = "http://172.16.4.40:8080/api/devices?limit=1000"

    token = GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers=headers)

    print (response)

    jsonObject = json.loads(response.text)
    jsonObject = json.dumps(jsonObject)

    print (jsonObject)
    return HttpResponse(jsonObject, content_type="application/json; charset = UTF-8")


def GetEndnodeDetails(request, id):

    endnode = Endnode.objects.get(id = id)
    url = "http://172.16.4.40:8080/api/devices/{}".format(endnode.dev_eui)

    token = GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers = headers)

    jsonObject = json.dumps(response.text)
    jsonObject = json.loads(jsonObject)

    return HttpResponse(jsonObject, content_type = "application/json; charset = UTF-8")

def AddEndNodeActivation(request, id):

    endnode = Endnode.objects.get(id=id)
    url = "http://172.16.4.40:8080/api/devices/{}/activate".format(endnode.dev_eui)

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    data = {
        "deviceActivation" : {
            "appSKey" : "string",
            "devAddr" : "string",
            "devEUI"  : "string",
            "fCntUp" : 0,
            "fNwkSIntKey" : "string",
            "nFCntDown" : 0,
            "nwkSEncKey" : "string",
            "sNwkSIntKey" : "string"
        }
    }

    response = request.post(url, headers = headers, data = data)

    print (response.text)
    print (response.status_code)

    return response.status_code

def GetEndNodeActivation(request, id):

    endnode = Endnode.objects.get(id=id)
    url = "http://172.16.4.40:8080/api/devices/{}/activation".format(endnode.dev_eui)

    token =GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers = headers)

    jsonObject = json.dumps(response.text)
    jsonObject = json.loads(jsonObject)

    return HttpResponse(jsonObject, content_type="application/json; charset = UTF-8")

def DeleteEndNodeActivation(request, id):

    endnode = Endnode.objects.get(id=id)
    url = "http://172.16.4.40:8080/api/devices/{}/activation".format(endnode.dev_eui)

    token = GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.delete(url, headers=headers)

    print (response.text)
    print (response.status_code)

    jsonObject = json.dumps(response.text)
    jsonObject = json.loads(jsonObject)

    return HttpResponse(jsonObject, content_type="application/json; charset = UTF-8")

"""