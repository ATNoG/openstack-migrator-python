from openstack import connection
from openstack.profile import Profile
import json

# profile
profile = Profile()
profile.set_version('identity', 'v2')

authentication_file = open('authentication.json', 'r')
auth_args = json.load(authentication_file)

conn = connection.Connection(profile=profile, **auth_args)

for compute in conn.compute.servers():
    print compute