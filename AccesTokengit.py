import requests
import json

app_id = 'xxxxxxxxxxxxxxxxx' #Application Id - on the azure app overview page
client_secret = 'xxxxxxxxxxxxxxxxxxxx' 
token_url = 'https://login.microsoftonline.com/xxxxxxxxxxxxx/oauth2/token'
crmwebapi = 'https://xxxxxxxxxxxxxxxx/api/data/v8.0' #full path to web api endpoint
#Query to select name and contact id 
crmwebapiquery = '/contacts?$select=fullname,contactid' #web api query (include leading /)
token_data = {
 'grant_type': 'password',
 'client_id': app_id,
 'client_secret': client_secret,
 'resource': 'https://xxxxxxxxx.dynamics.com/',
 'username':'xxxxxxxxxx.onmicrosoft.com', #Account with no 2MFA
 'password':'xxxxxxxxx',
}
token_r = requests.post(token_url, data=token_data)
token = token_r.json().get('access_token')
print("Access Token = "+  token)

accesstoken = token

if(accesstoken == token):
    #prepare the crm request headers
    crmrequestheaders = {
        'Authorization': 'Bearer ' + accesstoken,
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'Prefer': 'odata.maxpagesize=500',
        'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
    }
 
    #make the crm request
    crmres = requests.get(crmwebapi+crmwebapiquery, headers=crmrequestheaders)
 
    try:
        #get the response json
        crmresults = crmres.json()
 
        #loop through it
        for x in crmresults['value']:
            print (x['fullname'] + ' - ' + x['contactid'])
    except KeyError:
        #handle any missing key errors
        print('Could not parse CRM results')