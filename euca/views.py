from django.conf import settings
from django.shortcuts import render_to_response

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
  result = ""
 
  try:
    keyname = request.POST['keyname']
  except KeyError:
    keyname = None

  if keyname is None:
    result = "The key name field cannot be left blank. Please try again."
  else:
    try:
      new_key = EUCA.create_key_pair(keyname)
      key_path = settings.KEY_PATH + "/" + keyname + ".key"
      handle = open(key_path, 'w')
      handle.write(new_key.material)
      handle.close()

      result = "Key successfully added!"
    except boto.exception.EC2ResponseError:
      result = "There was a problem creating your Eucalyptus keypair. Please check your credentials and try again."
 
  return render_to_response('index.html', {'layout' : result})

def viewrunning(request):
  instances = []

  try:
    instances = EUCA.get_all_instances()
  except boto.exception.EC2ResponseError:
    pass

  return render_to_response('view.html', {'instances':instances})

def viewrunningpost(request):
  result = """
baz
"""
  return render_to_response('index.html', {'layout' : result})

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
  errors = []
  instance = []

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

  errors = []
  if keyname is None:
    errors.append("Key name cannot be left blank.")

  if image is None:
    errors.append("Image ID cannot be left blank.")

  if instance is None:
    errors.append("Instance type cannot be left blank.")

  if not errors:
    try:
      EUCA.run_instances(image_id, min_count=1, max_count=1, key_name=keyname, instance_type=instance_type)
    except boto.exception.EC2ResponseError:
      errors.append("There was a problem spawning your instance.")   

  return render_to_response('index.html', {'errors':errors, 'instance':instance})

def terminstance(request):
  result = "boo2"
  """
          <p />
          <label>New Key Name:</label>
          <br />
          <input name="title" size="40" type="text" />
          <input name="commit" type="submit" value="Add Key" />
"""
  return render_to_response('term.html', {'layout' : result})

def terminstancepost(request):
  """  try:
    keyname = request.POST['keyname']
  except KeyError:
    keyname = None

  errors = []
  if keyname is None:
    errors.append("Key name cannot be left blank.")

  if errors == []:
    # TODO: actually add the key and make sure it went through fine
    result = "Key successfully added!"
  else:
    result = "There were errors with your submission:<br /><br />"
    result += '<br /><br />'.join(errors)
"""

  result = "boo3"
  return render_to_response('index.html', {'layout' : result})


