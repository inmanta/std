require 'vagrant-openstack-provider'

Vagrant.configure('2') do |config|

  config.vm.provider :openstack do |os|
    os.openstack_auth_url = 'http://192.168.20.11:5000/v3'
    os.identity_api_version = '3'
    os.domain_name = "default"
    os.username           = ENV['OS_USERNAME']
    os.password           = ENV['OS_PASSWORD']
    os.tenant_name        = ENV['OS_USERNAME']
    os.project_name = ENV['OS_USERNAME']
    os.flavor             = 'c1m1'
    os.image              = '20180115-CentOS7-7.4'
    os.floating_ip_pool   = 'public'
    os.networks = 'jenkins'
  end

  config.vm.synced_folder ".", "/home/centos/std"
  config.ssh.username = 'centos'
  config.vm.provision :shell, path: "vagrant/centos_test_setup.sh"
end