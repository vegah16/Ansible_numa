# Ansible_numa
Ansible playbook for master's thesis.

## Install Ansible
1. Make sure that you can reach the remote server using ssh. If not, install `openssh-server`. Then, copy your key to the server for password-less login: `ssh-copy-id username@ip`.
2. Install using [this](https://docs.ansible.com/ansible/latest/installation_guide/index.html) link.
3. In your `/etc/ansible/hosts` file, inculde this where ubuntu is the group, and the username and ip must be replaced with your remote server info.

  [ubuntu]
  username@ip

## Run playbook
ansible-playbook suricata.yml --extra-vars "ansible_sudo_pass=root"
