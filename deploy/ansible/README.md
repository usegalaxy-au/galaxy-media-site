# Deployment with Ansible

### Install Ansible

See Ansible docs for more info:
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

```sh
sudo apt install ansible
# ~~~ or ~~~
python -m pip install ansible
```

---

### Application configuration

1. Modify the `hosts` file to match your webserver

1. Modify `playbook.yml` to reference the webserver you just created

1. Change the `letsencrypt_email` var in `group_vars/vars.yml`

1. Update webapp configuration in `group_vars/vars.yml` to suit:
   - Default admin login (please update these for security)
   - *Optional* - Host installation paths:
     - `project_root` - where this git repository will be cloned
     - `server_root` - where server configuration will be stored
     - `web_root` - where the application will be served from
     - `venv_root` - where the virtual env will be created

1. Create a `.env` file for the GMS webapp in the ansible root `./deploy/ansible` - please reference `.env.sample`

1. Create and encrypt three [Ansible secrets](https://docs.ansible.com/ansible/latest/user_guide/vault.html#encrypting-existing-files) in `group_vars/secrets.yml` (values should match your .env file):
  - For inital login to the admin site - `admin_email_secret`, `admin_password_secret`
  - Localhost database auth: `database_password_secret`

---

### Install

```sh
ansible-playbook -i hosts playbook.yml --vault-password-file /path/to/my/.vault.pass
```
