# Ansible_numa
Ansible playbook for master's thesis.

## Install Ansible
1. Make sure that you can reach the remote server using ssh. If not, install `openssh-server`. Then, copy your key to the server for password-less login: `ssh-copy-id username@ip`.
2. Install using [this](https://docs.ansible.com/ansible/latest/installation_guide/index.html) link.
3. In your `/etc/ansible/hosts` file, inculde the following, where ubuntu is the group, and the username and ip must be replaced with your remote server info.

```
[ubuntu]
username@ip
```

4. Install Ansible dependencies (Custom modules are added to env):

```
$ ansible-galaxy collection install community.general
```

## Execute playbook

### Configs
Every yml file in root folder is a specific config. To run test1.yml:

    ansible-playbook test1.yml

### Testing
In order to run the test run any playbook with the following tag:

    ansible-playbook test1.yml --tags "testing"

NB: Remember to change the variable `test_name: testX` to the correct test name. Result files will end up in the folder `results/testX`. You can set this var directly by running:

    ansible-playbook testing.yml -e "test_name=testX"
