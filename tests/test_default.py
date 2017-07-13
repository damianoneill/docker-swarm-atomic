#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
"""
File name: test_default.py.

Author: Damian ONeill
"""

import testinfra.utils.ansible_runner

runner = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory')

ALL = runner.get_hosts('all')
MANAGERS = runner.get_hosts('docker-swarm-managers')
WORKERS = runner.get_hosts('docker-swarm-workers')

testinfra_hosts = ALL


def test_docker_swarm_enabled(Command):
    """Test Swarm is eabled."""
    assert 'Swarm: active' in Command.check_output('sudo docker info')


def test_docker_swarm_status(Command, TestinfraBackend):
    """Test Swarm Status after deploying managers and workers."""
    docker_info = Command.check_output('sudo docker info')

    if TestinfraBackend.get_hostname() in MANAGERS:
        assert 'Is Manager: true' in docker_info
        assert 'Nodes: 3' in docker_info
        assert 'Managers: 2' in docker_info

    elif TestinfraBackend.get_hostname() in WORKERS:
        assert 'Is Manager: false' in Command.check_output('sudo docker info')


def test_docker_swarm_network(Command, TestinfraBackend):
    """Test Swarm Network is provisioned."""
    if TestinfraBackend.get_hostname() in MANAGERS:
        assert 'infra' in Command.check_output('sudo docker network ls')


def test_dockerlatest_running_and_enabled(Service):
    """Test docker latest is running."""
    dockerlatest = Service("docker-latest")
    assert dockerlatest.is_running
    assert dockerlatest.is_enabled


def test_docker_experimental_enabled(Command):
    """Test Experimental is eabled."""
    assert ' Experimental:    true' in \
        Command.check_output('sudo docker version')


def test_chrony_running_and_enabled(Service):
    """Test chrony latest is running."""
    chronyd = Service("chronyd")
    assert chronyd.is_running
    assert chronyd.is_enabled
