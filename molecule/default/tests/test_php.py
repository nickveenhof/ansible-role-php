import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name", [
    ("php5.6"),
    ("libapache2-mod-php5.6"),
    ("php5.6-mcrypt"),
    ("php5.6-cli"),
    ("php5.6-common"),
    ("php5.6-curl"),
    ("php5.6-dev"),
    ("php5.6-fpm"),
    ("php5.6-gd"),
    ("php-pear"),
    ("php-apcu"),
    ("php5.6-mysql"),
    ("libpcre3-dev"),
])
def test_packages(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_conf_directories(host):
    conf_path = host.file("/etc/php5/apache2")
    conf_ext_path = host.file("/etc/php5/apache2/conf.d")

    assert conf_path.is_directory
    assert conf_ext_path.is_directory


def test_php_conf(host):
    conf = host.file("/etc/php5/apache2/php.ini")

    assert conf.size == 4014
    assert conf.user == "root"
    assert conf.group == "root"
    assert conf.mode == 0o644


def test_apc_conf(host):
    conf = host.file("/etc/php5/apache2/conf.d/20-apcu.ini")

    assert conf.size == 82
    assert conf.user == "root"
    assert conf.group == "root"
    assert conf.mode == 0o644


def test_opcache_conf(host):
    conf = host.file("/etc/php5/apache2/conf.d/05-opcache.ini")

    assert conf.size == 251
    assert conf.user == "root"
    assert conf.group == "root"
    assert conf.mode == 0o644
