from config import get_config
from db import conn, get_services
from auth import get_keystone_client


class RegionBuilder(object):

    def __init__(self, config):
        self.regions = config.regions
        self.auth_info = config.auth
        self.keystone = get_keystone_client(self.auth_info)

    def get_region_services(self, region):
        mysql_uri = region.get('mysql_uri')
        services = get_services(conn(mysql_uri))
        return services

    def _create_endpoint(self, args):
        region_name = args['region_name']
        service_id = args['service_id']
        service_url = args['service_url']
        service_type = args['service_type']
        if service_url == '':
            return
        try:
            self.keystone.endpoints.create(region=region_name,
                                           service_id=service_id,
                                           publicurl=service_url,
                                           adminurl=service_url,
                                           internalurl=service_url)
            print "Success create endpoint for service: %s, at region: %s" % (service_type, region_name)

        except Exception as e:
            print 'Failed create endpoint for service: %s' % service_type
            print e

    def organize_endpoint_info(self, args):
        SERVICE_URL_MAP = {
            'compute': ':8774/v2/$(tenant_id)s',
            'volume': ':8776/v1/$(tenant_id)s',
            'volumev2': ':8776/v2/$(tenant_id)s',
            'image': ':9292',
            'network': ':9696/',
            'workflow': ':7303/v1/$(tenant_id)s',
            'maintenance': ':8071/v1',
            'cloudformation': ':8000/v1',
            'orchestration': ':8004/v1/$(tenant_id)s',
            'metering': ':8777/',
            'ec2': ':8773/services/Cloud',
            's3': ':3333'
        }
        service_type = args.get('service_type')
        base_url = args.get('base_url')
        route = SERVICE_URL_MAP.get(service_type, None)
        service_url = ''
        if not route:
            print 'Can not found url for %s' % service_type
        else:
            service_url = "%s%s" % (base_url, route)

        args['service_url'] = service_url
        return args

    def create_endpoint_by_services(self, services, region):
        for service in services:
            service_id, service_type = service
            if service_type == 'identity':
                # Pass identity endpoint create, use common
                continue
            params = {
                'service_type': service_type,
                'service_id': service_id,
                'region_name': region['name'],
                'base_url': region['base_url']
            }
            endpoint_info = self.organize_endpoint_info(params)
            self._create_endpoint(endpoint_info)

    def set_up(self):
        if (len(self.regions) == 0):
            print 'No region need to set up'

        for region in self.regions:
            services = self.get_region_services(region)
            self.create_endpoint_by_services(services, region)


def main():
    config = get_config()
    regions = config.regions
    builder = RegionBuilder(config)
    builder.set_up()

if __name__ == '__main__':
    main()
