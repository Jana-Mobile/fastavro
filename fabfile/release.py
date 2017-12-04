import os
from fabric.api import local, task, abort
from fabric.colors import yellow
import re


@task
def increment_version():
    if os.environ['JANAENV'] != 'leeroy':
        message = (
            "FastAvro can only be released from leeroy."
        )
        abort(yellow(message))

    local('git checkout master')
    local('git pull origin master')

    current_version = _extract_version_code()
    new_version = _increment_version(current_version)

    local(r"sed -i.orig 's/__version_info__ = \(.*\)/__version_info__ = \({}\)/' fastavro/__init__.py".
          format(', '.join([
              str(v) for v in new_version
          ])))
    local('git add fastavro/__init__.py')
    local('git commit -m "Update version to {}"'.format(new_version))

    local('git push origin master --tags')
    local('rm -f fastavro/__init__.py.orig')


def _extract_version_code():
    with open('fastavro/__init__.py', 'r') as f:
        for line in f:
            matches = re.search(
                '__version_info__ = \(\d*, \d*, \d*\)',
                line,
            )
            if not matches:
                continue
            version_tuple = matches.group(0).split("=")[1].strip()
            return (
                int(v) for v in
                version_tuple.replace('(', '').replace(')', '').split(',')
            )


def _increment_version(version):
    (major, minor, revision) = version
    return (major, minor, revision + 1)
