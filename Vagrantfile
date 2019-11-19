require 'vagrant-openstack-provider'

Vagrant.configure('2') do |config|

  config.vm.provider :openstack do |os|
    os.openstack_auth_url = ENV['OS_AUTH_URL']
    os.identity_api_version = '3'
    os.domain_name = "default"
    os.username           = ENV['OS_USERNAME']
    os.password           = ENV['OS_PASSWORD']
    os.tenant_name        = ENV['OS_USERNAME']
    os.project_name = ENV['OS_USERNAME']
    os.flavor             = 'c1m1'
    os.image              = 'ssh_and_python'
    os.floating_ip_pool   = ENV['OS_FLOATING_IP_POOL']
    os.networks = ENV['OS_NETWORK']
  end

  config.vm.synced_folder ".", "/home/centos/std", type: "rsync"
  config.ssh.username = 'centos'
  config.vm.provision :shell, path: "vagrant/centos_test_setup.sh", env: {"GIT_LOCAL_BRANCH" => ENV["GIT_LOCAL_BRANCH"]}
end