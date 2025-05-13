import sys
import os
import json
import requests
import csv
import boto3
from botocore.exceptions import ClientError
from requests_toolbelt.multipart.encoder import MultipartEncoder
import dateutil.parser
from datetime import datetime, timedelta, time, timezone
from dateutil import tz
from pytz import UTC as utc
import pytz
from tqdm.auto import tqdm
import pandas as pd


global g_username
global g_password
global g_api_url_base
global g_token

global g_s3_data_bucket_upload
global g_exec_t
global g_WAF_Tag

class PSCommon:
    def __init__(self, env):
        self.env = env
        self.cfg = ps_set_env(env)

    def __str__(self):
        return  self.env
    
    def get_env(self):
        return self.cfg

    def login(self):
        return ps_login()

    def get(self, get_url):
        return ps_get(get_url)

    def get_account(self, acc):
        return ps_get_account(acc)
    
    def set_account(self, accid, accinfo):
        return ps_set_account(accid, accinfo)

    def get_all_accounts(self):
        return ps_get_all_accounts()

    def get_all_mp_from_account(self, account, with_partners_mp = False):
        return ps_get_all_mp_from_account(account, with_partners_mp)
    
    def get_all_mp_from_accounts(self, account_list, with_partner_mp = False):
        return ps_get_all_mp_from_accounts(account_list, with_partner_mp)

    def get_all_mps_from_all_accounts(self, includeRetired=False):
        return ps_get_all_mps_from_all_accounts(includeRetired=False)

    def get_all_mps_from_all_accounts_as_df(self, includeRetired=False):
        return ps_get_all_mps_from_all_accounts_as_df(includeRetired)

    def get_event_mp(self,accountId, mpId,startDate,endDate,deviceEventTypeId):
        return ps_get_event_mp(accountId, mpId,startDate,endDate,deviceEventTypeId)

    def get_event_mp_alarm_evt_notes_status(self,request):
        return get_event_mp_alarm_evt_notes_status(request)

    def get_mp(selfs, mp):
        return ps_get_mp(mp)

    def get_mp_trend(self,mp,payload):
        return ps_get_mp_trend(mp,payload)

    def get_mp_channel_def(self,mp):
        return ps_get_mp_channel_def(mp)

    def get_mp_parameters(self,mp):
        return ps_get_mp_parameters(mp)
    
    def get_maxLoadCurrentDemand(self,mp):
        return ps_get_maxLoadCurrentDemand(mp)

    def get_mp_heartbeat(self,mp,max):
        return ps_get_mp_heartbeat(mp,max)

    def get_mp_by_serial(selfs,serialNumber):
        return ps_get_mp_by_serial(serialNumber)

    def get_site(self,siteId):
        return ps_get_site(siteId)

    def get_activity_log(self, activity, start, end, url=None):
        return ps_get_activigy_log(activity, start, end, url)

    def get_maintenance_history(self, mpId):
        return ps_get_maintenance_history(mpId)

    def set_site(self,accountId, sideId, site):
        return ps_set_site(accountId, sideId, site)

    def set_site_mp(self,accountId, siteId, measurementPointId, site_mp):
        return ps_set_site_mp(accountId, siteId, measurementPointId, site_mp)

    def get_exec_t(self):
        return g_exec_t

    def get_user(self):
        return g_username

    def get_apiurl(selfs):
        return g_api_url_base

    def set_working_dir(self, working_dir):
        os.makedirs(working_dir, exist_ok=True)
        os.chdir(working_dir)

    def post_cmd(self,mpId,cmd):
        return ps_post_cmd(mpId,cmd)

    def device_file_request_by_mp(self, mp, files):
        return ps_device_file_request_by_mp(mp,files)
    
    def firmware_set_version_to_device(self, version, devices):
        return ps_firmware_set_version_to_device(version, devices)
    
    def firmware_start(self, devices):
        return ps_firmware_start(devices)

    def firmware_search(self, query="?count=100000&offset=0&search=&excludeOnline=false&excludeOffline=true"):
        return ps_firmware_search(query)

    def get_notification_groups(self):
        return ps_get_notification_groups()

    def get_notification_group(self, ng):
        return ps_get_notification_group(ng)

    def catchup(self, request, mp):
        return ps_catchup(request, mp)

    def device_file_request(self,request):
        return ps_device_file_request(request)
    
    def post(self, url, request):
        return ps_post(url, request)


class PSS3:
    def __init__(self, profile=None):
        if profile is not None:
            self.session = boto3.session.Session(profile_name=profile)
            self.s3_client = self.session.client('s3')
            if g_aws_key == 'from_cli' and g_aws_secret == 'from_cli':
                self.s3_resource = boto3.resource('s3', region_name='us-east-1')
            else:
                self.s3_resource = boto3.resource('s3', region_name='us-east-1')
        else:
            self.s3_client = boto3.client('s3')

        self.bucket = g_s3_data_bucket_upload

    def get_bucket_name(self):
        return g_s3_data_bucket_upload

    def set_bucket_name(self, bucket_name):
        global g_s3_data_bucket_upload
        g_s3_data_bucket_upload = bucket_name

    def download_file(self, file_name, object_name=None):
        # If s3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
            
        try:
            response = self.s3_client.download_file(self.bucket, file_name, file_name)
            #print(f's3 Download: {response}')
        except ClientError as e:
            print(f's3 download error {e}')
            return False
        return True

    def download_folder(self, local_folder):
        # os.makedirs(local_folder, exist_ok=True)
        b = self.s3_client.Bucket(self.bucket)
        try:
            for obj in b.objects.filter(Prefix=local_folder):
                if not os.path.exists(os.path.dirname(obj.key)):
                    os.makedirs(os.path.dirname(obj.key))
                b.download_file(obj.key, obj.key)  # save to same path

        except ClientError as e:
            print(f's3 download dir error {e}')
            return False
        return True

    def download_date_range(self, local_folder, beg_date, end_date):
        #os.makedirs(local_folder, exist_ok=True)
        total = 0
        b = self.s3_client.Bucket(self.bucket)
        try:
            keys = [
                o for o in b.objects.filter(Prefix=local_folder)
                if o.last_modified < end_date and o.last_modified >= beg_date
            ]
            total = len(keys)
            pbar = tqdm(range(total), position=0, leave=True)
            for i in pbar:
                if not os.path.exists(os.path.dirname(keys[i].key)):
                    os.makedirs(os.path.dirname(keys[i].key))
                b.download_file(keys[i].key, keys[i].key)
                pbar.set_description(f'{keys[i].key}')
                if i == (total -1): pbar.set_description(f'Downloading')

        except ClientError as e:
            print(f's3 download dir error {e}')
            return -1
        return total

    def upload_file(self, file_name, object_name=None):
        # If s3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)
        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, self.bucket, object_name)
            # print(f's3 Upload: {response}')
        except ClientError as e:
            print(f's3 upload error {e}')
            return False
        return True


def ps_set_env(environment):
    global g_username
    global g_password
    global g_api_url_base
    global g_s3_data_bucket_upload
    global g_aws_key
    global g_aws_secret
    global g_exec_t
    global g_WAF_Tag

    env = {}

    try:
        f = open('pypscloud_cfg.json', 'r')
        cfg = json.load(f)
        for e in cfg:
            if (e['env'] == 'production') and (environment == 'production' or environment == 'prod'):
                env = e
                break
            elif e['env'] == 'staging' and environment == 'staging':
                env = e
                break

    except OSError as e:
        print(f"{type(e)}: {e}")
        return

    if env == None:
        print(f'Error in reading pypscloud_cfg.json, looking for production or staging, case sensitive')
        return

    if env.get('user'):
        g_username = env['user']
    if env.get('pw'):
        g_password = env['pw']
    if env.get('base_url'):
        g_api_url_base = env['base_url']
    if env.get('data_bucket_upload'):
        g_s3_data_bucket_upload = env['data_bucket_upload']
    if env.get('aws_key'):
        g_aws_key = env['aws_key']
    else:
        g_aws_key = "from_cli"
    if env.get('aws_secret'):
        g_aws_secret = env['aws_secret']
    else:
        g_aws_secret = "from_cli"

    if env.get('WAF_Tag'):
        g_WAF_Tag = env['WAF_Tag']
    else:
        g_WAF_Tag = ""

    g_exec_t = datetime.today().strftime('%Y%m%d-%H%M')
    return env


def ps_login():
    global g_token
    request = {
            "email": g_username,
            "password": g_password}

    response = requests.post(g_api_url_base + 'login', json=request, headers={'X-Internal-Service': g_WAF_Tag})
    if response.status_code == 200:
        info = response.json()
        g_token = info["token"]
    else:
        print(response)
    return response.status_code


def ps_get(get_url):
    api_url = f'{g_api_url_base}{get_url}'
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    return requests.get(api_url, headers=header)


def ps_get_all_accounts():
    api_url = '{0}accounts?count={1}'.format(g_api_url_base, 100000)
    accounts = []

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        accounts = response.json()
    else:
        print(response)

    return accounts


def ps_get_account(accid):
    api_url = f'{g_api_url_base}account/{accid}'

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)

    return None


def ps_set_account(accid, payload):
    api_url = f'{g_api_url_base}account/{accid}'

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    response = requests.put(api_url, headers=header, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)

    return None



def ps_get_all_mp_from_accounts(account_list, with_partners_mp = False):
    all_mps = []
    for acc in account_list:
        mps = ps_get_all_mp_from_account(acc, with_partners_mp)
        all_mps.extend(mps)
    return all_mps


def ps_get_all_mp_from_account(account, with_partners_mp = False):
    '''
    Measurement Point
    {'accountId': 252, 'accountName': 'Dominion Energy', 'partnerId': 252, 'partnerName': 'Dominion Energy', 'measurementPointId': 15802, 'measurementPointTypeId': 1, 'measurementPointStatusId': 8, 'measurementPointTypeName': 'QubeScan', 'measurementPointStatusName': 'commissioned', 'mainImageId': None, 'commissionedWhen': '2023-01-30T20:35:00.000Z', 'lastCommunicationTime': '2023-10-04T18:20:00.000Z', 'isLocked': 1, 'mpId': 'Afton Chemical 2.5', 'serialNumber': 'P3018306', 'pqubeModel': 'PQube3', 'notes': '', 'locationId': 1895, 'createdWhen': '2023-01-30T20:34:53.000Z', 'locationName': 'Afton Chemical', 'locationShortname': 'Afton Chemical', 'address1': '500 Spring Street', 'address2': '', 'city': 'Richmond', 'state': 'VA', 'zipCode': '23219', 'country': 'United States', 'latitude': 37.541115523, 'longitude': -77.44778955, 'siteInformation': None, 'timezone': 'America/New_York', 'summaryKpi': '#FF0000', 'acInputKpi': '#FF0000', 'psuKpi': '#4BB050', 'dcBusKpi': '#4BB050', 'acOutputKpi': '#4BB050', 'severeEventCount': 3}
    '''
    mps = []
    if type(account) is dict:
        if "id" in account:
            acId = account["id"]
            if acId == 2: #getting rid of Powerside Manufacturing
                return mps
    elif type(account is int):
        acId = account
    else:
        return mps
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = '{0}measurementPoints/hierarchy?accountId={1}{2}'.format(g_api_url_base, acId,"&excludeMeasurementPoints=false&excludeMeasures=true&includeRetired=false" )

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        #Parse json
        customersList = []
        keepCustomers = True
        mpinfoDict = response.json()
        #hierarchie call return diff structure based on partner or customer.
        if "partners" in mpinfoDict:
            if len(mpinfoDict["partners"]) == 1:
                customersList = mpinfoDict["partners"][0]["customers"]
            else:
                print(f'Error long partner list {mpinfoDict["partners"]}')
            if with_partners_mp == False: keepCustomers = False

        elif "customers" in mpinfoDict:
            customersList = mpinfoDict["customers"]

        if customersList != None:
            for custDict in customersList:
                for mp in custDict["measurementPoints"]:
                    if mp['accountId'] == mp['partnerId'] or keepCustomers == True: #this is to avoid adding mp from a customer with a partner twice.
                        mps.append(mp)

    else:
        print(response)
    return mps


def ps_get_all_mps_from_all_accounts(includeRetired=False):
    '''
    return the big dict with everything
    '''
    print("get_all_mps_from_all_accounts")
    includeRetiredFlag = "true"
    if includeRetired == False:
        includeRetiredFlag = "false"
    api_url = f'{g_api_url_base}measurementPoints/hierarchy?excludeMeasurementPoints=false&excludeMeasures=true&includeRetired={includeRetiredFlag}'
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None


def ps_get_all_mps_from_all_accounts_as_df(includeRetired=False):
    '''
    return the big dict with everything as a dataframe
    '''
    print("get_all_mps_from_all_accounts_as_df")
    df = pd.DataFrame()
    all = ps_get_all_mps_from_all_accounts(includeRetired)
    if all is not None:
        if 'partners' in all:
            all_p = all['partners']
            for p in all_p:
                for customer in p['customers']:
                    for m in customer['measurementPoints']:
                        mdf = pd.DataFrame([m])
                        df = pd.concat([df,mdf],ignore_index=True)
    else:
        print(f'ps_get_all_mps_from_all_accounts returned None')

    return df



def ps_get_mp(mpId):
    '''
    parameter mpId:
    get the measurement point information
    {
        "mpId": "Rada Entrance - 01",
        "roomId": 7,
        "measurementPointTypeId": 2,
        "measurementPointStatusId": 8,
        "commissionedWhen": "2019-11-22T22:46:52.000Z",
        "crmCode": null,
        "notes": "",
        "accountId": 5,
        "city": "Delson",
        "country": "Canada",
        "timezone": "America/Toronto",
        "accountName": "Rada Industries",
        "measurementPointTypeName": "In-Site",
        "measurementPointStatusName": "commissioned",
        "locationName": "sitename",
        "serialNumber": "P3001234"


    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}measurementPoint/{mpId}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        mp = response.json()
        mp['measurementPointId'] = mp['roomId']         #addind this field since most of other calls are using measurementPointId, not roomId
        return mp
    else:
        print(f'get_mp: {response}')
        return None


def ps_get_site(siteId):
    '''
    parameter siteId:
    get the site information
    {
      "locationId": 1648,
      "locationName": "PQube3 e Test wall 02",
      "shortname": "Engineering wall",
      "address1": "7850 Route Transcanadienne",
      "address2": "",
      "city": "Montréal",
      "state": "QC",
      "zipCode": "H4T 1A5",
      "country": "Canada",
      "latitude": 45.48768810000001,
      "longitude": -73.7137436,
      "siteInformation": null,
      "clientId": 4966,
      "clientName": "",
      "siteContactName": null,
      "siteContactPhone": null,
      "siteContactEmail": null,
      "measurementPoints": [
        {
          "roomId": 13817,
          "mpId": "PQube3 e Test CloudTeam",
          "roomNumber": null,
          "measurementPointTypeId": 1,
          "measurementPointStatusId": 8,
          "measurementPointEmailCode": 89781,
          "measurementPointEmailAddress": "8b1494d2f67b90d155d87f8324874b60",
          "notes": "",
          "crmCode": null,
          "equipmentId": 9998,
          "equipmentType": null,
          "equipmentDisplayOrder": null,
          "sid": null,
          "modelNumber": null,
          "serialNumber": null,
          "modalityDesc": null
        }
      ]
    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}site/{siteId}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        site = response.json()
        return site
    else:
        print(f'ps_get_site: {response}')
        return None


def ps_set_site(accountId, siteId, site):
    #print(f'ps_set_site {site}')
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    #BE does not support these values
    if site['siteInformation'] == None:
        site['siteInformation'] = ""
    if site['siteContactName'] == None:
        site['siteContactName'] = ""
    if site['siteContactPhone'] == None:
        site['siteContactPhone'] = ""
    if site['siteContactEmail'] == None:
        site['siteContactEmail'] = ""


    response = requests.put(g_api_url_base + f'site/{siteId}?accountId={accountId}', json=site, headers=header)
    if response.status_code == 200:
        info = response.json()
    else:
        print(response)
        print(response.status_code)
        print(response.headers)
        print(response.reason)
    return response.status_code


def ps_set_site_mp(accountId, siteId, measurementPointId, site_mp):
    '''
    :param accountId
    :param site_mp = 
        {
          "site": {
            "locationName": "move to",
            "shortname": "move to",
            "address1": "1683-1, Prieur Est",
            "address2": "",
            "city": "Montréal",
            "state": "PQ",
            "zipCode": "H2C 1M5",
            "country": "Canada",
            "siteInformation": "",
            "latitude": 45.5667066,
            "longitude": -73.6578514
          },
          "measurementPoint": {
            "mpId": "M1-rename",
            "measurementPointTypeId": 1
          },
          "parameters": null
        }
    '''

    # print(f'ps_set_site {site}')
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.patch(g_api_url_base + f'site/{siteId}/measurementPoint/{measurementPointId}?accountId={accountId}', json=site_mp, headers=header)
    if response.status_code != 200:
        print(response)
        print(response.status_code)
        print(response.headers)
        print(response.reason)
    return response.status_code


def ps_get_mp_channel_def(mp):
    '''
    {
      "pqubeModel": "PQube 3e",
      "nominalFrequency": "60",
      "nominalPhaseToNeutralVoltage": "346.4",
      "powerConfiguration": "Wye/Star",
      "lockTime": "2023-11-09T07:27:09.000Z",
      "createdBy": 2,
      "nominalPhaseToPhaseVoltage": "207.8",
      "createdWhen": "2023-11-09T15:32:17.190Z",
      "measurementPointId": "86354717",
      "firmwareVersion": "daily_11_06_2023_2346"
      "channels": {
        "0": {
          "3": {
            "channelScalar": 0.03509521484375,
            "unitOffset": 3,
            "isConfigurable": false,
            "name": "N-E 3PLD2",
            "units": "V",
            "trendTable": {
              "oneminute": [
                "c_3_min_v",
                "c_3_avg_v",
                "c_3_max_v"
              ]
            },
            "meterParam": "c_3_inst_v"
          },
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    #api_url = f'{g_api_url_base}channelDefinition/{mp}?eligibleForTrendAlertsOnly=false'
    api_url = f'{g_api_url_base}channelDefinition/{mp}?channelType=trend&defaultFallback=QubeScan'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_mp_channel_def: {response}')
        return None


def ps_get_mp_parameters(mp):
    '''
    {
        "measurementPointId": "15206",
        "content": {
            "ratedCurrent": {
                "unit": "A",
                "defaultValue": 500,
                "editable": true,
                "hint": {
                    "en": "Max 15min demand current over the previous 12month period. Can be estimated if not measured. A decent estimation is feeding transformer current rating."
                },
                "description": {
                    "en": "Input rated current, or max demand current"
                },
                "title": {
                    "en": "Rated Current"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": 500
            },
            "contractedPower": {
                "unit": "kW",
                "defaultValue": 1000,
                "editable": true,
                "hint": {
                    "en": "Exceeding the contracted power by more than X % may trigger penalties charged in the next utility bills."
                },
                "description": {
                    "en": "Maximum power agreed with Utility"
                },
                "title": {
                    "en": "Contracted power"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": 1000
            },
            "maxPowerDemandThreshold": {
                "unit": "kW",
                "defaultValue": 1000,
                "editable": true,
                "hint": {
                    "en": "Threshold for the  15min max/peak power demand. Used to to trigger a hight power demand alarm in In-Site."
                },
                "description": {
                    "en": "Threshold"
                },
                "title": {
                    "en": "Max power demand threshold"
                },
                "validationRegEx": "^(\\d+.?\\d*|0|None)$",
                "value": 1000
            },
            "nominalPhaseToNeutralVoltage": {
                "unit": "V",
                "defaultValue": 2400,
                "editable": false,
                "hint": {
                    "en": "Nominal Phase to Neutral Voltage."
                },
                "description": {
                    "en": "Nominal Phase to Neutral Voltage"
                },
                "title": {
                    "en": "Nominal Phase to Neutral Voltage"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": "266.0"
            },
            "powerFactorThreshold": {
                "defaultValue": 0.9,
                "editable": true,
                "hint": {
                    "en": "Threshold for the  15min power factor. Used to to trigger an low power factor alarm in In-Site."
                },
                "description": {
                    "en": "Lowest Power factor agreed with Utility"
                },
                "title": {
                    "en": "Lowest Power factor agreed with Utility"
                },
                "validationRegEx": "^[0-1]\\.[0-9]$",
                "value": 0.9
            },
            "nominalFrequency": {
                "unit": "Hz",
                "defaultValue": 60,
                "editable": false,
                "hint": {
                    "en": "Nominal Frequency"
                },
                "description": {
                    "en": "Nominal Frequency"
                },
                "title": {
                    "en": "Nominal Frequency"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": 60
            },
            "powerConfiguration": {
                "description": {
                    "en": "Power Configuration"
                },
                "title": {
                    "en": "Power Configuration"
                },
                "value": "Wye/Star",
                "editable": false,
                "defaultValue": "STAR",
                "hint": {
                    "en": "Power Configuration"
                }
            },
            "groundCurrentThreshold": {
                "unit": "A",
                "defaultValue": 1,
                "editable": true,
                "hint": {
                    "en": "Threshold for the 1/2 cycle max ground current.Used to evaluate the Ground_Current alarm notification"
                },
                "description": {
                    "en": "Maximum peak ground current "
                },
                "title": {
                    "en": "Ground current threshold"
                },
                "validationRegEx": "^(\\d+.?\\d*|0|None)$",
                "value": 1
            },
            "outputRated": {
                "unit": "A",
                "defaultValue": 500,
                "editable": true,
                "hint": {
                    "en": "Max 15min demand current over the previous 12month period. Can be estimated if not measured. A decent estimation is feeding transformer current rating."
                },
                "description": {
                    "en": "Output rated current"
                },
                "title": {
                    "en": "Output rated current"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": 500
            },
            "nominalPhaseToPhaseVoltage": {
                "unit": "V",
                "defaultValue": 4160,
                "editable": false,
                "hint": {
                    "en": "Nominal Phase to Phase Voltage."
                },
                "description": {
                    "en": "Nominal Phase to Phase Voltage"
                },
                "title": {
                    "en": "Nominal Phase to Phase Voltage"
                },
                "validationRegEx": "^\\d+.?\\d*$",
                "value": "460.0"
            }
        }
    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}parameters/{mp}?includeDefinition=true'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_mp_parameters: {response}')
        return None


def ps_get_mp_by_serial(serialNumber):
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}device/{serialNumber}/measurementPointInfo'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_mp_by_serial: {response}')
        return None


def ps_post_cmd(mpId, cmd):
    # print(f'ps_post_cmd mpId:{mpId} cmd:{cmd}')
    url = f'{g_api_url_base}measurementPoint/{mpId}/maintenance'
    sessionId=""

    mp_encoder = MultipartEncoder(fields={"parameters": json.dumps({"commandId":cmd})})
    header = {'authorization': 'Bearer ' + g_token, 'Content-Type': mp_encoder.content_type}

    response = requests.post(url, data=mp_encoder, headers=header)
    if response.status_code == 200:
        info = response.json()
        sessionId = info["id"]
    else:
        print(f'error ps_post_cmd:{mpId}')
        print(response)
    return sessionId


def ps_get_maintenance_history(mpId):
    '''
    [
      {
        "id": 1,
        "maintenanceRequestId": 10039,
        "firmwareVersionId": null,
        "commandId": 9,
        "command": "getDiagnostic",
        "measurementPointId": 20656,
        "parameters": "{\"in\":\"\",\"out\":null}",
        "statusId": 3,
        "status": "succeeded",
        "response": {
          "documentId": 17218460
        },
        "statusChangedAt": "2024-07-15T18:06:29.000Z",
        "createdBy": "julie ma",
        "createdAt": "2024-07-15T18:05:49.000Z"
      },
      {
        "id": 2,
        "maintenanceRequestId": null,
        "firmwareVersionId": 13691,
        "commandId": null,
        "command": "firmwareUpdate",
        "measurementPointId": 20656,
        "parameters": "{\"in\":\"\",\"out\":null}",
        "statusId": 4,
        "status": "Completed",
        "response": "3.10.7.24.05.16",
        "statusChangedAt": "2024-05-28T05:06:20.000Z",
        "createdBy": "Louis Marchand",
        "createdAt": "2024-05-28T04:49:59.000Z"
      },
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}measurementPoint/{mpId}/maintenance'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_maintenance_history: {response}')
    return None


def ps_export_list_to_CSV(f,the_list,field_names, write_header=True, mode='w'):
    t = datetime.today().strftime('%Y%m%d-%H%M')
    file_name = f'{f}-{t}.csv'
    with open(file_name, mode, encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        if write_header:
            writer.writeheader()

        writer.writerows(the_list)
        csvfile.close()
    return


def ps_ (accountId, mpId,startDate,endDate,deviceEventTypeId):
    '''
    [
      {
        "documentId": 2628579,
        "deviceEventId": 359793,
        "triggeredWhen": "2023-10-04T15:20:26.741Z",
        "deviceEventTypeId": 2,
        "eventMagnitude": null,
        "eventMagnitudeTag": null,
        "channel": null,
        "channelId": null,
        "duration": null,
        "isSevere": 0,
        "deviceEventType": "snapshot",
        "defaultDisplayName": null,
        "timezone": "America/St_Johns",
        "gifDocumentExists": 1,
        "pqdDocumentExists": 0,
        "csvDocumentExists": 1,
        "waveformDocumentId": 2628581,
        "rmsDocumentId": 2628583,
        "deviceEventStatus": "unread",
        "isCleared": 0,
        "sagDirectionPrediction": null,
        "sagDirectionProbability": null
      }
    ]
    '''

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    if deviceEventTypeId != 0:
        api_url = f'{g_api_url_base}events/measurementPoint/{mpId}?accountId={accountId}&dateRangeStart={startDate}&dateRangeEnd={endDate}&deviceEventTypeId={deviceEventTypeId}&severeOnly=false&includeRetired=false&offset=0&count=100000'
    else:
        api_url = f'{g_api_url_base}events/measurementPoint/{mpId}?accountId={accountId}&dateRangeStart={startDate}&dateRangeEnd={endDate}&severeOnly=false&includeRetired=false&offset=0&count=100000'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'get_mp: {response}')
        return None


def  ps_get_mp_trend(mpId ,payload):
    '''
    :param mpId: measurement Point as integer
    :param payload: the request
    :return: url or json object depending of the request in the payload
    '''
    api_url = f'{g_api_url_base}trends/measurementPoint/{mpId}'
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    res = requests.post(api_url, json=payload, headers=header)
    if  res.status_code !=  200:
        print(res.status_code)
        print(res.headers)
        print(res.reason)
        print(payload)
        return None
    return res.text


def ps_download_file(file_name, bucket, object_name=None):
    '''
    Upload a file to an s3 bucket
    :param file_name: File to download
    :param bucket: Bucket to upload to
    :param object_name: s3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    '''

    # If s3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.download_file(bucket, file_name, file_name)
        #print(f's3 Download: {response}')
    except ClientError as e:
        print(f's3 download error {e}')
        return False
    return True


def ps_upload_file(file_name, bucket, object_name=None):
    """Upload a file to an s3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: s3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If s3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        #print(f's3 Upload: {response}')
    except ClientError as e:
        print(f's3 upload error {e}')
        return False
    return True


def ps_convert_date_to_iso(date_str):
    '''
    #assume date into that format yyyy-mm-ddTHH:MM:SS.MMMZ, will return yyyy-mm-dd HH:MM:SS

    :param date_str:
    :return date in iso format:
    '''
    begin = date_str[0:10]
    end = date_str[11:19]
    return begin + " " + end


def ps_time_with_tz(utc_string, to_tz):
    from_zone = tz.tzutc()
    to_zone = tz.gettz(to_tz)
    utc = datetime.strptime(utc_string, '%Y-%m-%dT%H:%M:%S.000Z')
    utc = utc.replace(tzinfo=from_zone)
    local_time = utc.astimezone(to_zone)
    return local_time

def ps_time_utc_to_local(utc_string, to_tz):
    # 2023-12-08T18:56:18.000Z
    from_zone = tz.tzutc()
    to_zone = tz.gettz(to_tz)
    utc = datetime.strptime(utc_string, '%Y-%m-%dT%H:%M:%S.000Z')
    utc = utc.replace(tzinfo=from_zone)
    local_time = utc.astimezone(to_zone)
    return local_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def ps_time_local_to_utc(local_string, from_tz):
    # 2023-12-08T18:56:18.000Z
    from_zone = tz.gettz(from_tz)
    to_zone = tz.tzutc()
    local = datetime.strptime(local_string, '%Y-%m-%dT%H:%M:%S.000Z')
    local = local.replace(tzinfo=from_zone)
    local_time = local.astimezone(to_zone)
    return local_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def ps_build_start_end_date_from_midnight(days, tz):
    '''
    return string time in utz 2024-01-26T08:00:00.000Z, based on the requested tz
    :param days: range from today's midnight
    :param tz: origin tz.
    '''

    req_endtime = datetime.now()
    req_endtime = req_endtime.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = timedelta(days=days)
    req_starttime = req_endtime - delta

    req_endtime_str = req_endtime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    req_starttime_str = req_starttime.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    req_endtime_str = ps_time_local_to_utc(req_endtime_str,tz)
    req_starttime_str = ps_time_local_to_utc(req_starttime_str, tz)
    
    return req_starttime_str, req_endtime_str


def ps_build_start_end_date_from_now(days=1):
    req_endtime = datetime.utcnow()
    delta = timedelta(days=days)
    req_starttime = req_endtime - delta

    req_endtime_str = req_endtime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    req_starttime_str = req_starttime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return req_starttime_str, req_endtime_str


def ps_device_file_request_by_mp(mp, files):
    # print("ps_device_file_request_by_mp")
    request = {
        "measurementPointId": mp,
        "files": files
    }

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + 'file/device/request', json=request, headers=header)
    if response.status_code == 200:
        info = response.json()
    else:
        print(response)
    return response.status_code


def ps_get_mp_heartbeat(mp, max):
    '''
    return list of heart beat informatoin
    :param mp: mp
    :param max: number of heart beat to retreive

    [
      {
        "internalTemperature": "48.6°C",
        "time": "2024-01-30T20:44:14.407Z",
        "gpsLock": null,
        "measurementPointId": "86354717"
      },
      {
        "internalTemperature": "48.7°C",
        "time": "2024-01-30T20:43:14.235Z",
        "gpsLock": null,
        "measurementPointId": "86354717"
      },
    ...
    ]
    '''

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}measurementPoint/heartbeat/{mp}?limit={max}'


    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_mp_heartbeat: {response}')
        return None


def ps_get_maxLoadCurrentDemand(mpId):
    '''
    parameter mpId:
    get maxLoadCurrentDemain
    {
        "coverage": 97.80821917808218,
        "maxDemandLoadCurrent": 39.48061111111111,
        "details": {
            "2023-04": {
                "partial": true,
                "value": 13.886666666666667
            },
            "2024-04": {
                "partial": true,
                "value": 23.069333333333336
            },
            "2023-05": {
                "value": 26.964666666666666
            },
            "2023-06": {
                "value": 44.48333333333333
            },
            "2023-07": {
                "value": 20.826000000000004
            },
            "2023-08": {
                "value": 43.896666666666675
            },
            "2023-09": {
                "value": 56.644
            },
            "2023-10": {
                "value": 27.340666666666667
            },
            "2023-11": {
                "value": 54.48533333333333
            },
            "2023-12": {
                "value": 44.839999999999996
            },
            "2024-01": {
                "value": 55.50266666666666
            },
            "2024-02": {
                "value": 54.236000000000004
            },
            "2024-03": {
                "value": 26.069999999999997
            }
        }
    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}trends/maxLoadCurrentDemand/measurementPoint/{mpId}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_maxLoadCurrentDemand: {response}')
        return None


def ps_firmware_set_version_to_device(version, devices):
    # print("ps_set_firmware_version_to_device")
    request = devices

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + 'firmwareVersion/setToDevices/' + version, json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None


def ps_firmware_start(devices):
    '''
    devices: list of device measurement points
    returns:
    [
      {
        "id": 12763,
        "measurementPointId": 13,
        "version": "3.10.6.24.02.01",
        "status": "Uploading"
      }
    ]
    '''
    # print("ps_firmware_start")
    request = devices

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + 'firmware/update/start', json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None


def ps_firmware_search(query="?count=100000&offset=0&search=&excludeOnline=false&excludeOffline=true"):
    '''
    query to be used
    {
      "records": [
        {
          "mpId": "Kawailoa Mauka 46kV Sw Sta",
          "measurementPointId": 12333,
          "measurementPointTypeId": 1,
          "lastCommunicationTime": "2024-02-29T15:06:46.000Z",
          "online": 1,
          "measurementPointTypeName": "QubeScan",
          "siteId": 1560,
          "siteName": "Kawailoa Mauka 46kV Sw Sta",
          "accountId": 100,
          "location": "Haleiwa, HI, United States",
          "accountName": "Hawaiian Electric",
          "useFirmwareAutomaticUpdates": 0,
          "partnerAccountId": null,
          "partnerAccountName": null,
          "requestId": 12695,
          "currentFirmwareVersion": "3.9.12.22.05.16",
          "requestFirmwareVersion": "3.10.5.23.11.28",
          "responseFirmwareVersion": "3.10.5.23.11.28",
          "status": "Completed",
          "validationReason": "Firmware Applied",
          "requestCreatedWhen": "2024-01-22T23:24:36.000Z",
          "requestCreatedById": 381,
          "requestCreatedByFirstName": "Tracy",
          "requestCreatedByLastName": "Yamamoto",
          "requestCreatedByEmail": "tracy.yamamoto@hawaiianelectric.com",
          "timezone": "Pacific/Honolulu",
          "pqubeModel": "PQube 3",
          "tz": "HST"
        }...
      ],
      "firmwareVersions": [
        "daily_02_22_2024_1936",
        "3.10.6.24.02.01",
        "3.10.6.24.01.29",
        "3.10.6.24.01.23",
        "3.10.5.23.11.28",
        "3.10.4.23.10.12",
        "3.10.3.23.07.14",
        "3.10.1.23.02.24",
        "3.10.0.22.11.10",
        "3.9.13.22.08.15",
        "3.9.13.22.08.09"
      ],
      "totalRecordCount": 611
    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}firmware/fleetStatus/search{query}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_firmware_search_online: {response}')
    return None


def ps_get_notification_groups():
    '''
    will return:
    {
      "records": [
        {
          "notificationGroupId": 157,
          "name": "BasicGroup-002",
          "isDisabled": 0,
          "customerAccount": "Test Basic Account",
          "partnerAccount": "Partner Example"
        },
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}notificationGroup?offset=0&count=20'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_notification_groups: {response}')
    return None


def ps_get_notification_group(ng):
    '''
    {
      "notificationGroupId": 157,
      "accountId": 7447,
      "name": "BasicGroup-002",
      "isDisabled": 0,
      "cloudTrendAlert": 0,
      "deviceSystemEvents": 0,
      "measurementPoints": [
        {
          "id": 86351020,
          "mpId": "Place Bell-01"
        }
      ],
      "measurementPointsFromAccounts": [],
      "recipientsAsUser": [
        {
          "userId": 11720,
          "firstName": "BasicE",
          "lastName": "BasicE",
          "mobilePhone": "",
          "email": "software.powerside+basic-e@gmail.com"
        },
        {
          "userId": 11721,
          "firstName": "BasicV",
          "lastName": "BasicV",
          "mobilePhone": "",
          "email": "software.powerside+basic-v@gmail.com"
        }
      ],
      "recipientsAsCustom": [],
      "eventTypes": [
        {
          "id": 54,
          "name": "Interruptions"
        }
      ]
    }
    '''
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}notificationGroup/{ng}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_notification_group: {response}')
    return None


def ps_get_activigy_log(activity, start, end, url=None):
    print(f'ps_get_activigy_log for {activity}')
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}
    api_url = f'{g_api_url_base}activityLogs/search?activity={activity}&offset=0&count=150000&includeDeviceUsage=true&startDateRange={start}&endDateRange={end}'

    response = requests.get(api_url, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'ps_get_activigy_log: {response}')
    return None


def ps_catchup(catchup_req, mp):
    '''
       catchup_req: {
                      "dateRangeStart": "2024-07-01T00:00:00.000Z",
                      "dateRangeEnd": "2024-07-08T00:00:00.000Z",
                      "calculateOnly": true,
                      "entireRange": false,
                      "startCatchup": false
                    }
       returns:
       [
          {
            "gapStart": "2024-02-05T14:50:00.000Z",
            "gapEnd": "2024-02-09T18:30:00.000Z",
            "gapPackets": 599
          },
          {
            "gapStart": "2024-03-10T06:50:00.000Z",
            "gapEnd": "2024-03-10T06:50:00.000Z",
            "gapPackets": 1
          }
       ]
       '''
    # print("ps_get_catchup")
    request = catchup_req

    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + f'trends/catchup/{mp}', json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None


def ps_device_file_request(request):
    '''
    {
        "measurementPointId": 0,
        "files": ["string"]
    }
    '''

    # print("ps_device_file_request")
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + f'file/device/request', json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None


def get_event_mp_alarm_evt_notes_status(request):
    '''
    {
      "measurementPointId": 9240,
      "dateRangeStart": "2024-06-01T07:00:00.000Z",
      "dateRangeEnd": "2024-10-03T06:59:00.000Z",
      "natures": [
        "event",
        "status"
      ],
      "typeIds": [
        "s1"
      ],
      "includeRetired": false,
      "includeLabels": true,
      "sorting": [
        {
          "column": "triggeredWhen",
          "desc": true
        }
      ],
      "count": 20,
      "offset": 0
    }
    '''

    # print("ps_device_file_request")
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + f'measurementPoint/alarmsEventsNotes', json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None


def ps_post(url, request):

    # print("ps_post")
    header = {'authorization': 'Bearer ' + g_token, 'X-Internal-Service': g_WAF_Tag}

    response = requests.post(g_api_url_base + url, json=request, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(response)
    return None