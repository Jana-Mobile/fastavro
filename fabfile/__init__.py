import release

from fabric.api import local, task

assert release


@task(default=True)
def list_tasks():
    local('fab --list')
