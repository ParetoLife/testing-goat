import uuid
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

env.use_ssh_config = True
REPO_URL = "https://github.com/ParetoLife/testing-goat"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _download_source()
        _update_dependencies()
        _update_env()
        _update_static_files()
        _update_database()


def _download_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_dependencies():
    if not exists("./venv/bin/pip"):
        run("python3.6 -m venv venv")
    run("./venv/bin/pip install -r requirements.txt")


def _update_env():
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = str(uuid.uuid4())
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")


def _update_static_files():
    run("./venv/bin/python manage.py collectstatic --noinput")
    # We need to move these static files to a location where nginx can access
    # them. In our OS version (Amazon Linux 1) nginx is not allowed to access
    # these files directly from our repo.
    run("cp -r ./static/* /var/www/testing-goat")


def _update_database():
    run("./venv/bin/python manage.py migrate --noinput")
