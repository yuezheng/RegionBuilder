from keystoneclient.v2_0 import client

def get_keystone_client(auth_info):
    username = auth_info['username']
    password = auth_info['password']
    tenant_name = auth_info['tenant_name']
    auth_url = auth_info['url']
    try:
        keystone = client.Client(username=username,
                                 password=password,
                                 tenant_name=tenant_name,
                                 auth_url=auth_url)
    except Exception as e:
        print "Error at get keystone client"
        print '----'
        print e
        print '----'

    return keystone
