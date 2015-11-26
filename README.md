#RegionBuilder
----

##A tool for simplify the process of set multi region

###The process of set multi region is:
    1. Deploy two or more openstack environment;
    2. Update all service (nova/cinder/glance/ceilometer .etc) config file,
        set auth_token segment point to a common keystone;
    3. Create endpoints for each service from different env at the common keystone;

###The third process is the most messy and fallible, so I want write a script to handle that.
