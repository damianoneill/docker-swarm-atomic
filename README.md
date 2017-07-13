docker-swarm-atomic
=========

An Ansible role that configures Docker Swarm (>=1.12) on Centos [Atomic Host](http://www.projectatomic.io/download/)

A swarm cluster is dependent on an accurate time source, so an option is provided to configure chrony(ntp) as part of the role.

Requirements
------------

Ensure that your Ansible hosts are running [Atomic](https://wiki.centos.org/SpecialInterestGroup/Atomic/Download/) >= 7.20170428

Role Variables
--------------

````
# Configure chrony in the swarm
docker_swarm_config_chrony: false
docker_swarm_chrony_servers: []
# - 0.pool.ntp.org
# - 1.pool.ntp.org

# Option of substituting the atomic host’s default docker 1.12 container engine
# with a more recent, docker 1.13-based version, provided via the docker-latest package
docker_latest: false

# Enable the experimental flag on dockerd, docker_latest needs to be enabled as well
docker_experimental: false

docker_swarm_addr: "{{ hostvars[inventory_hostname]['ansible_' + docker_swarm_interface]['ipv4']['address'] }}"
docker_swarm_interface: "enp0s8"
docker_swarm_port: "2377"

# Configure docker networks in the swarm
docker_swarm_config_networks: false
docker_swarm_networks: []
  # - name: "infra"
  #   driver: "overlay"
  #   state: "present"
  # - name: "proxy"
  #   driver: "overlay"
  #   state: "absent"

# Define Ansible group which contains your Docker swarm managers
docker_swarm_managers_ansible_group: 'docker-swarm-managers'

# Defines first node in docker_swarm_managers_ansible_group as primary
docker_swarm_primary_manager: '{{ groups[docker_swarm_managers_ansible_group][0] }}'


# Define Ansible group which contains you Docker swarm workers
docker_swarm_workers_ansible_group: 'docker-swarm-workers'
````

Dependencies
------------

None

Example Playbook
----------------

```
- hosts: all
  vars:
    - docker_swarm_interface: "enp0s8"
    - docker_latest: true
    - docker_experimental: true
    - docker_swarm_config_networks: true
    - docker_swarm_networks:
      - name: "infra"
        driver: "overlay"
        state: "present"
    - docker_swarm_config_chrony: true
    - docker_swarm_chrony_servers:
      - 0.pool.ntp.org
      - 1.pool.ntp.org
  roles:
    - role: docker-swarm-atomic
```

Test
----

Solution uses [molecule](https://molecule.readthedocs.io/en/master/) and vagrant, ensure that both are installed locally

````
pip install molecule
pip install python-vagrant
````

The tests can then executed manually with

````
molecule test
````

The solution requires a full operating system to test, hence the use of vagrant rather than docker.  Subsequently no automation of the tests can be done through travis as travis doesn't support virtualbox.

License
-------

Apache

Author Information
------------------

Damian ONeill

* https://github.com/damianoneill
