"""
from django.shortcuts import render, HttpResponse, redirect
from .forms import GatewayForm
from .models import Gateways, GatewayInternalInformations
from django.contrib import messages
from django.contrib.auth.models import User
import requests, json, dateutil.parser
from datetime import datetime, timedelta


def ListGateways(request):

    userNames = []

    token = GetTokenFromLoraAPI("yagizhanyakali", "8546Yny")

    gateways = GetAllGateways(token)

    Gateways.objects.all().delete()

    for gateway in gateways:
        try:
            gatewayInternal = GatewayInternalInformations.objects.get(gatewayEui = str(gateway[2]))
            print("Try")
            gatewayType = gatewayInternal.typeofGatewayInternal
            addedUser = gatewayInternal.author
            gatewayModel = Gateways(gatewayName = gateway[0], gatewayDescription = gateway[1], gatewayEui = gateway[2], gatewayCreatedDate = gateway[3], gatewayLastSeen = gateway[4], typeofGateway = gatewayType, author = addedUser)

        except GatewayInternalInformations.DoesNotExist:
            gatewayModel = Gateways(gatewayName = gateway[0], gatewayDescription = gateway[1], gatewayEui = gateway[2], gatewayCreatedDate = gateway[3], gatewayLastSeen = gateway[4])
            print("Except")
        gatewayModel.save()

    gateways = Gateways.objects.all()

    context = {
        "gateways": gateways
    }

    return render(request, "gateway_index.html", context=context)


def GetAllGateways(token):

    gatewayNames =[]
    gatewayDescriptions = []
    gatewayEuis = []
    gatewayCreatedDates = []
    gatewayLastSeens = []

    url = "http://169.254.1.3:8888/gateways/all/"

    headers = {
        "Authorization": "Token {}".format(token)
    }

    response = requests.get(url, headers=headers)

    #print(response.text)

    for gateway in json.loads(response.text)["result"]:

        gatewayNames.append(gateway["name"])
        gatewayDescriptions.append(gateway["description"])
        gatewayEuis.append(gateway["id"])

        createdDate = dateutil.parser.parse(gateway["createdAt"])
        createdDate = datetime.strptime(str(createdDate)[:-13], r'%Y-%m-%d %H:%M:%S')
        createdDate = createdDate + timedelta(hours=3)
        gatewayCreatedDates.append(str(createdDate))

        gatewayLastSeens.append(gateway["lastSeenAt"])

    return zip(gatewayNames, gatewayDescriptions, gatewayEuis, gatewayCreatedDates, gatewayLastSeens)

def GetTokenFromLoraAPI(username, password):

    url = "http://169.254.1.3:8888/api-token-auth/"

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)

    token = json.loads(response.text)["token"]

    return token


def AddGateway(request):

    form = GatewayForm(request.POST or None)
    if form.is_valid():

        gateway = form.save(commit=False)
        gateway.author = request.user
        gatewayIndoor = request.POST.get("indoor", False)
        gatewayOutdoor = request.POST.get("outdoor", False)
        if (gatewayIndoor == "indoor" and gatewayOutdoor == False):
            typeofGateway = "Indoor"
        if (gatewayOutdoor == "outdoor" and gatewayIndoor == False):
            typeofGateway = "Outdoor"
        if (gatewayIndoor == False and gatewayOutdoor == False):
            typeofGateway = "Indoor"
        gateway.typeofGateway = typeofGateway
        gateway.gatewayStatus = "Connected"

        createGatewayResponse = CreateGateway(gateway.gatewayName, gateway.gatewayDescription, gateway.gatewayEui)

        #internalDb = GatewayInternalInformations(gatewayEui = gateway.gatewayEui, typeofGatewayInternal = typeofGateway, author = request.user)
        #internalDb.save()

        print (createGatewayResponse)

        if (createGatewayResponse == "OK"):
            messages.add_message(request, messages.SUCCESS, "Gateway Added!")
            gateway.save()
        else:
            messages.add_message(request, messages.ERROR, "Progress Error!")

        return render(request, "add_gateway.html")
    return render(request, "add_gateway.html", {"form": form})


def CreateGateway(gatewayName, gatewayDescription, gatewayEui):

    url = "http://172.16.4.40:8080/api/gateways"
    token = GetTokenFromLoraAPI()
    profileID = GetProfileID(token)

    print (token)
    print (profileID)

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    data = {
        "gateway": {
            "description": str(gatewayDescription),
            "gatewayProfileID": str(profileID),
            "id": str(gatewayEui),
            "location": {
	            "accuracy": 0,
	            "altitude": 0,
	            "latitude": 0,
	            "longitude": 0,
	            "source": "UNKNOWN"
            },
	    "name": str(gatewayName),
	    "networkServerID": "2",
	    "organizationID": "1"
        }
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    print (response.text)
    print (response.status_code)

    if (response.status_code == 200):
        return "OK"
    else:
        return "Error"

def UpdateGateway(gatewayName, gatewayDescription, gatewayEui):

    url = "http://172.16.4.40:8080/api/gateways/{}".format(gatewayEui)

    token = GetTokenFromLoraAPI
    profileID = GetProfileID(token)

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    data = {
        "gateway": {
            "description": str(gatewayDescription),
            "gatewayProfileID": str(profileID),
            "id": str(gatewayEui),
            "location": {
                "accuracy": 0,
                "altitude": 0,
                "latitude": 0,
                "longitude": 0,
                "source": "UNKNOWN"
            },
            "name": str(gatewayName),
            "networkServerID": "2",
            "organizationID": "1"
        }
    }

    data = json.dumps(data)

    print(data)

    response = requests.put(url, headers=headers, data=data)

    if (response.status_code == 200):
        return "OK"
    else:
        return "Error"


def EditGateway(request, id):

    gateway = Gateways.objects.get(id = id)

    context = {
        "gateway": gateway
    }

    if (request.method == "POST"):

        gatewayTypeIndoor = request.POST.get("indoor", False)
        gatewayTypeOutdoor = request.POST.get("outdoor", False)
        if (gatewayTypeIndoor == "indoor" and gatewayTypeOutdoor == False):
            typeofGateway = "Indoor"
        if (gatewayTypeOutdoor == "outdoor" and gatewayTypeIndoor == False):
            typeofGateway = "Outdoor"
        if (gatewayTypeIndoor == False and gatewayTypeOutdoor == False):
            typeofGateway = "Indoor"
        gateway.typeofGateway = typeofGateway

        
        #try:
#    internalGateway = GatewayInternalInformations.objects.get(gatewayEui = str(gateway.gatewayEui))
#    internalGateway.typeofGatewayInternal = typeofGateway
#      internalGateway.save()
      #  except GatewayInternalInformations.DoesNotExist:
#    internalGateway = GatewayInternalInformations(gatewayEui = gateway.gatewayEui, typeofGatewayInternal = typeofGateway)
#    internalGateway.save()


        gateway.save()

        updateGatewayResponse = UpdateGateway(str(gateway.gatewayName), str(gateway.gatewayDescription), str(gateway.gatewayEui))

        print (updateGatewayResponse)

        return redirect("/gateways/")
    return render(request, "edit_gateway.html", context=context)


def DeleteGateway(request, id):

    gateway = Gateways.objects.get(id = id)

    context = {
        "gateway": gateway
    }

    if(request.method == "POST"):
        print("Delete Progress Started!")

        gatewayEui = gateway.gatewayEui

        url = "http://172.16.4.40:8080/api/gateways/{}".format(gatewayEui)

        token = GetTokenFromLoraAPI()

        headers = {
            "Grpc-Metadata-Authorization": str(token)
        }

        response = requests.delete(url, headers=headers)

        responseInternal = Gateways.objects.get(id=id).delete()

        return redirect("http://127.0.0.1:8000/gateways/")
    
    return render(request, "delete_gateway.html", context=context)


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


def GetProfileID(token):

    url = "http://172.16.4.40:8080/api/gateway-profiles?limit=5"

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers=headers)

    jsonObject = json.loads(response.text)
    profileID = jsonObject["result"][0]["id"]

    return str(profileID)

def GetGatewayDetails(request, id):

    gateway = Gateways.object.get(id = id)
    url = "http://172.16.4.40:8080/api/gateway/{}".format(gateway.gatewayEui)
    token = GetTokenFromLoraAPI()

    headers = {
        "Grpc-Metadata-Authorization": str(token)
    }

    response = requests.get(url, headers = headers)

    jsonObject = json.dumps(response.text)
    jsonObject = json.loads(jsonObject)

    return HttpResponse(jsonObject, content_type="application/json; charset = UTF-8")
"""