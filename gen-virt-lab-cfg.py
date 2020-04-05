#!/usr/bin/python

OSES = (
    'centos6',
    'centos7',
    'centos8',
    'debian10',
    'debian9',
    'fedora31',
    'opensuse15',
    'ubuntu1804',
)

print('# Auto Generated - Do Not Edit')
print('')
print('#-------------------------------------------------------------------')
print('# Package installs')
print('#-------------------------------------------------------------------')
print('')

count = 1
for os in OSES:
  lab = 'ta%02d' % count
  print('[%s]' % lab)
  print('desc = %s' % (os))
  print('distro = %s' % os)
  print('''\
postcreate = ansible-playbook -i {scriptdir}/inventory.sh {playbookdir}/local-dns.yaml
  {playbookdir}/wait.yaml {playbookdir}/testcell.yaml && ssh %s01 run-openafs-robotest.sh tests
group.afs_cell = 1
group.afs_clients = 1
group.afs_kdcs = 1
group.afs_databases = 1
group.afs_fileservers = 1
group.afs_robotest = 1
var.afs_bosserver_opts = -pidfiles''' % lab)
  print('')
  count += 1

count = 1
for version in ('master', 'openafs-stable-1_8_x'):
  print('#-------------------------------------------------------------------')
  print('# Build %s' % version)
  print('#-------------------------------------------------------------------')
  print('')
  for os in OSES:
    lab = 'tb%02d' % count
    print('[%s]' % lab)
    print('desc = %s build %s' % (os, version))
    print('distro = %s' % os)
    print('''\
postcreate = ansible-playbook -i {scriptdir}/inventory.sh {playbookdir}/local-dns.yaml
  {playbookdir}/wait.yaml {playbookdir}/testcell.yaml && ssh %s01 run-openafs-robotest.sh tests
group.afs_cell = 1
group.afs_clients = 1
group.afs_kdcs = 1
group.afs_databases = 1
group.afs_fileservers = 1
group.afs_robotest = 1
var.afs_bosserver_opts = -pidfiles
var.afs_selinux_mode = permissive
var.afs_server_install_method = rsync
var.afs_server_build_force = no
var.afs_server_build_builddir = /usr/local/src/openafs_server
var.afs_server_build_destdir = /tmp/openafs_server
var.afs_server_build_fetch_method = git
var.afs_server_build_git_repo = git://{ gateway }/openafs
var.afs_server_build_git_ref = %s
var.afs_client_install_method = rsync
var.afs_client_build_force = no
var.afs_client_build_builddir = /usr/local/src/openafs_server
var.afs_client_build_destdir = /tmp/openafs_server
var.afs_client_build_fetch_method = git
var.afs_client_build_git_repo = git://{ gateway }/openafs
var.afs_client_build_git_ref = %s''' % (lab, version, version))
    print('')
    count += 1
