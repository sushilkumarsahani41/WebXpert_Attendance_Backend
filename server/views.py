import json
import os
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files.storage import default_storage as store
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from .Crypt import Crypt
import shutil
from django.views.decorators.csrf import csrf_exempt



config = {
  "type": "service_account",
  "project_id": "webxpertattendance",
  "private_key_id": "8ea28815f72ad6055655cb32e8beffb15dffe2fe",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCgA1wYbxnV9PzG\ne7ulMNSdl2hnj+4990vetJpCO4E7AMXQpEXhJxyl3/lIy4zij/zV3JyQtNFT3sXj\nkms8qvOFyncM/0U1CG9hfXgOiU+ZIZcVsqaYFbKjv5Imka4shDzlthwjLDKkAUTm\nqKgnOroo8tUc7vnZPR2JF7PCN5VBtasXgRIIRxvhhVSwH8pXG6G1obv2nP3+kDLd\nkg1p1Xk4E8wYwJ99NZ7tTmsqVuMIBOCKy+SEeKbWUT1FzN0yQCDSWFHkZ+ztWPwz\nCXENH2ASvQS6YQnxqFHAFBVlq61rNI9IwxryfGsTyMzMp4x0BzKSxxQtaU4Vptm3\niRaWYYnLAgMBAAECggEAJCuuQU24At/+1eU5bSWFIlyL+sET40kICv87UZZ+53YM\nwVWpADTlqm9fO//bSImw5y0X7TQaj4FvrTo3aH7iTo+Oas83dz4BY4HHxk1uw1hO\n/VYlh4J8H7zZzkMnIqP/2hNY9/BxQBaTWyqr3DZPx5rg5sn0i5FfoFJNzazf3frV\n+bc0BHRJnhIxInQMW4NjQWP4p3cP5OXbxZVvHNyYwkifYL9sOlpFOZMez97NlL7Q\nt/niG+zV54MmT9VtKoBXui1mXuJM208NJKqgne7cuRvIjjLrbIBdla1Di8ZCozHX\n/IVqFlgnXQoAIb3fG5E4tGInuW+M66o4H9PCQ30LwQKBgQDPzS4R7JO/qqyRjCQy\nOSHOX56lGMhPBnupP71ogAE23prIL8vkIukkb42NqkEhhk/e6l9XReMQpmsRCErw\nZt1EhrY5cjm97qsuUwawy1/oDAJ2o8G+YD2MO3l/QZgQAMmlGzFfQezYPAR769D7\ntexFmKHXt/nr335n3IOhK5OHwQKBgQDFIJs4PaJNoc6N/gX3N/GsVokC6t123nmZ\nTt+CmR4YminwAVePBhmlnfd26mRN/JBJRBoWnjk1chLGx2RgJGWukj0S2dVvo4kD\n31c9C8Ow8sUROrirVlJlZ2KnnFe6HEsdofRKNH4FlMXyK0X1DmJSzvtE2MZx0hXA\nQ7DGT5vUiwKBgBWs3UVZW//+GYoFCDGE7BXOu4mVEC/OCVAaKfOghn/msFZ5RddC\nHPeD+0vvmmOY0vP5loBP9eNiuIBKUSbKVAI12wQa+hLptklat7PxQsu9lPQzGJ53\nA3SBL6cqfGYO7vmd4ISDJ+VWPVF/w4i97StFRHxv4E3OPi0vPzusg/MBAoGBAL72\n12ekTZbnKTJk42Kaz4QkUJaC8Ag3fZUG03+w1Xb/4aCfrDLhtfa7EQAiEQl7oktX\nre47WTBtUcM/Zf29RMPY51FbtWhxBEq8EccRnoHMrRwDxuI0vZ1+ihPVYSbqQdpz\nCjTYpTzC4v+27A554MZXvRL07UlWO7wF1zpF5LABAoGADFkeusb18erwTmLuFpvF\nFRow/gt8gcvsOsaGuJjU84BSfcdGH+Ai+vMF4yyzSvvzklcPJr/fIXoPi8Wx0MxG\n78PfI2MxBB3WH46hQxYofLvric6qzxWujWKbz0HtiLYmRcZ9N5Kzjx0f1wV5R9gN\nCmP4OsIZj7SNIsGg61+Ar5w=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-o59sa@webxpertattendance.iam.gserviceaccount.com",
  "client_id": "114164580275715954192",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-o59sa%40webxpertattendance.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
APIkey ='9tVwVRQhXEZG8u4f3pJTPeFoleAskSSPvcF_kAqGv08ZGINTiFIkLZ6AOcKQumXoOUO6ZazHYoo68ype1uyGiA'
cred = credentials.Certificate(config) 
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def heartBeat(request):
    if request.method == 'GET':
        deviceID = request.GET.get('deviceID')
        key = request.GET.get('key')
        if key == APIkey:
            db.collection("devices").document(deviceID).update({'lastSeen':firestore.SERVER_TIMESTAMP})
    
    return JsonResponse({'status' : 200, 'message' : "HeartBeat Recieved Successfully"})


def getEnrollment(request):
    if request.method == 'GET':
        deviceID = request.GET.get('deviceID')
        key = request.GET.get('key')
        if key == APIkey:
            res = db.collection("enrollment").document(deviceID).get()
            data = res.to_dict()
            return JsonResponse(data)
        return JsonResponse({'status' : 200, 'message' : "Action Not Permitted"})                


def updateEnrollment(request):
    if request.method == 'GET':
        deviceID = request.GET.get('deviceID')
        key = request.GET.get('key')
        if key == APIkey:
            enrolledID = request.GET.get('enrolledID')
            data = {
                'last_enroll_id': enrolledID,
                'enroll' : False,
                'lastUpdate': firestore.SERVER_TIMESTAMP
            }
            db.collection('enrollment').document(deviceID).update(data)
            return JsonResponse({'status' : 200, 'message' : "Enrollement Updated"})   

def genDeviceConfig(request):
    if request.method == 'GET':
        deviceID = request.GET.get('deviceID')
        key = request.GET.get('key')
        if key == APIkey:
            dt = db.collection('devices').document(deviceID).get()
            d = dt.to_dict()
            del d['lastSeen']
            d["deviceID"] = deviceID
            depid = d["departmentID"]
            subData = db.collection('departments').document(depid).get()
            sub = subData.to_dict()['subjects']
            d['subjects'] = sub
            data = json.dumps(d)
            encrypted_data = Crypt(data).encrypt()
            if os.path.exists(deviceID):
                shutil.rmtree(deviceID)
            os.mkdir(deviceID)
            with open(f'{deviceID}/config.wxcfg', 'wb') as cfg:
                cfg.write(encrypted_data)
                cfg.close()
            res = FileResponse(open(f'{deviceID}/config.wxcfg', 'rb'))
            res['Content-Disposition'] = f'attachment; filename="config.wxcfg"'
            return res


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        deviceID = request.POST.get('deviceID')
        uploaded_file = request.FILES.getlist('file')
        if uploaded_file:
            print(uploaded_file)
            print(deviceID)
            for f in uploaded_file:
                store.save(f'{deviceID}/{f.name}',f)
            file = os.path.join(os.curdir,f'media/{deviceID}/{f.name}')
            with open(file, 'rb') as cfg:
                data = Crypt(cfg.read()).decrypt()
                print(json.loads(data))
            return JsonResponse({'status': 200, 'message': 'File successfully uploaded'})      
        
    return JsonResponse({'status': 404, 'message': 'Something went wrong'}) 