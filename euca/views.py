from django.conf import settings
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import HttpResponse
import simplejson
json = simplejson
import boto
import os
import re

# bad way to do this - should put it in a separate file
# but since this is a small demo project it is ok for now

# validate env vars here

ACCESS_KEY = os.environ.get("EC2_ACCESS_KEY")
if ACCESS_KEY:
  pass
else:
  raise NameError("The EC2_ACCESS_KEY environment variable was not set. Please set it and try again.")

SECRET_KEY = os.environ.get("EC2_SECRET_KEY")
if SECRET_KEY:
  pass
else:
  raise NameError("The EC2_SECRET_KEY environment variable was not set. Please set it and try again.")

EC2_URL = os.environ.get("EC2_URL")
if EC2_URL:
  pass
else:
  raise NameError("The EC2_URL environment variable was not set. Please set it and try again.")

# also a bad idea - the ec2 lib is only pulled in once connect_ec2 is called
# but i need regioninfo for euca, so call connect_ec2 and catch the exception
# that's thrown to get euca support
# TODO: check if this is fixed in boto2.0
try:
  boto.connect_ec2()
except AttributeError:
  pass

hostname = re.search("http://(.*):8773/services/Eucalyptus", EC2_URL).group(1)
region = boto.ec2.regioninfo.RegionInfo(name="eucalyptus", endpoint=hostname)

EUCA = boto.connect_ec2(aws_access_key_id=ACCESS_KEY,
                       aws_secret_access_key=SECRET_KEY,
                       is_secure=False,
                       region=region,
                       port=8773,
                       path="/services/Eucalyptus")

# Create your views here.

def addkeypair(request):
  key_names = []

  try:
    key_pairs = EUCA.get_all_key_pairs()
    key_names = [key.name for key in key_pairs]
  except boto.exception.EC2ResponseError:
    pass

  return render_to_response('add.html', {'keys' : key_names})

def addkeypairpost(request):
  result = {}
  result["success"] = "true"
  error = "" 
  try:
    keyname = request.POST['keyname']
  except KeyError:
    keyname = None

  if keyname is None:
    error = "The key name field cannot be left blank. Please try again."
  else:
    try:
      new_key = EUCA.create_key_pair(keyname)
      key_path = settings.KEY_PATH + "/" + keyname + ".key"
      handle = open(key_path, 'w')
      handle.write(new_key.material)
      handle.close()

      # chmod the key so that ssh will accept it
      os.chmod(key_path, 0600)

      result["name"] = keyname
    except boto.exception.EC2ResponseError, e:
      error = "There was a problem adding your key. <p style='color: red;'>" + str(e) + "</p>"
  if error:
    result["success"] = "false" 
    result["error"] = error
  return HttpResponse(json.dumps(result)) 

def viewrunning(request):
  reservations = []

  try:
    reservations = EUCA.get_all_instances()
  except boto.exception.EC2ResponseError:
    pass

  return render_to_response('view.html', {'reservations':reservations})

def viewrunningpost(request):
  error = ""
  result = {}
  result["success"] = "true"
  keyname = ""
  public_ip = ""
  regex = r"[^\w\d/\.-]"
  pattern = re.compile(regex)
  try:
    public_ip = request.POST['public_ip']
    public_ip = pattern.sub('', public_ip)
  except KeyError:
    error = "Missing Public IP."
  try:
    keyname = request.POST['keyname']
    keyname = pattern.sub('', keyname)
  except KeyError:
    error = "Missing keyname."

  if not error:
    keypath = settings.KEY_PATH + "/" + keyname + ".key"
    command = "nohup xterm -e 'ssh -i " + keypath + " root@" + public_ip + "' &"
    os.popen(command)
  if error: 
    result["error"] = error    
    result["success"] = "false"

  return HttpResponse(json.dumps(result)) 

def runinstance(request):
  machines = []
  keys = []

  try:
    images = EUCA.get_all_images()
    for image in images:
      if image.type == "machine":
        machines.append(image)
  except boto.exception.EC2ResponseError:
    pass

  all_files = os.listdir(settings.KEY_PATH)
  for f in all_files:
    filename, extension = os.path.splitext(f)
    if extension == ".key":
      keys.append(filename)

  return render_to_response('run.html', {'images': machines, 'keys': keys})

def runinstancepost(request):
  ret = {}
  ret["success"] = "true"
  error = ""
  instance_id = ""
  try:
    keyname = request.POST['key_to_use']
  except KeyError:
    keyname = None

  try:
    image_id = request.POST['image_to_run']
  except KeyError:
    image_id = None

  try:
    instance_type = request.POST['instance_type']
  except KeyError:
    instance_type = None

  if keyname is None:
    error = "Key name cannot be left blank."
  elif image_id is None:
    error = "Image ID cannot be left blank."
  elif instance_type is None:
    error ="Instance type cannot be left blank."
   
  if not error:
    try:
      reservation = EUCA.run_instances(image_id, min_count=1, max_count=1, key_name=keyname, instance_type=instance_type)
      for instance in reservation.instances:
        instance_id = instance.id
    except boto.exception.EC2ResponseError, e:
      error = "There was a problem spawning your instance. <p style='color: red;'>" + str(e) + "</p>"

  if error:
    ret["success"] = "false"
    ret["error"] = error
  else:
    ret["instance_id"] = instance_id 
  return HttpResponse(json.dumps(ret)) 

def terminstance(request):
  reservations = []

  try:
    reservations = EUCA.get_all_instances()
  except boto.exception.EC2ResponseError:
    pass

  return render_to_response('term.html', {'reservations':reservations})

def terminstancepost(request):
  error = ""
  result = {}
  result["success"] = "true"
  try:
    instance_id = request.POST['instance']
  except KeyError:
    instance_id = None
    error = "Please specify an image to connect to."
  if not error:
    EUCA.terminate_instances([instance_id])
  else:
    result["error"] = error
    result["success"] = "false"

  return HttpResponse(json.dumps(result)) 

