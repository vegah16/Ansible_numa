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
For now, when running the playbook for the first time, you have to use the option "-K" so that you can enter the root password. After this, the playbook can run without entering the password.

**TODO: improve this?**

**Initial execution**

    ansible-playbook suricata.yml -K

**Subsequent executions**
  
    ansible-playbook suricata.yml
