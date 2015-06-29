from openstack import connection
import json

authentication_file = open('authentication.json', 'r')
auth_args = json.load(authentication_file)

conn = connection.Connection(**auth_args)

projects = conn.identity.list_projects()

pass