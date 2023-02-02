import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/edseldim/TDDPractice.git"

def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _register_service()

def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"ls -ltra && git reset --hard {current_commit}")

def _update_virtualenv():
    if not exists(".venv/bin/pip"):
        run(f"/home/elaucho/.pyenv/shims/python -m virtualenv .venv")
    run("./.venv/bin/python -m pip install -r requirements.txt")

def _create_or_update_dotenv():
    append(".env","DJANGO_DEBUG_FALSE=y")
    append(".env",f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices(
            "abcdefghijklmnopqrstuvwxyz0123456789", k = 50
        ))
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")

def _update_static_files():
    run("./.venv/bin/python manage.py collectstatic --no-input")

def _update_database():
    run("./.venv/bin/python manage.py migrate --no-input")

def _register_service():
    run("cat ./deploy_tools/nginx.template.conf | sed 's/DOMAIN/165.22.8.89/g' | sudo tee /etc/nginx/sites-available/165.22.8.89")
    run("sudo ln -s /etc/nginx/sites-available/165.22.8.89 /etc/nginx/sites-enabled/165.22.8.89")
    run("cat ./deploy_tools/gunicorn-systemd.template.service \
    | sed 's/DOMAIN/165.22.8.89/g' \
    | sudo tee /etc/systemd/system/gunicorn-165.22.8.89.service")
    run("sudo systemctl daemon-reload")
    run("sudo systemctl nginx")
    run("sudo systemctl enable gunicorn-165.22.8.89")
    run("sudo systemctl start gunicorn-165.22.8.89")