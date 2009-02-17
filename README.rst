Polinax 
=========
A free site with the modest aim of modernizing democracy. Polinax is written in Python
using the Django and Pinax projects as a base. Please join the discussion Group_.

.. _Group: http://groups.google.com/group/polinax

PINAX BASED DIRECTORY STRUCTURE

projects/
    polinax/            currently includes the laws and notification apps
apps/
    external_apps/      external re-usable apps via svn:externals
    local_apps/         re-usable apps that aren't yet externalized
libs/
    external_libs/      contains external libraries
docs/                   documentation (using rst and sphinx; in progress)
fixtures/               test fixtures (in progress)

There is some path manipulation in manage.py to get this all to work. You'll
need to do something similar in your wsgi or mod_python configuration.

To install the required external libraries and pass run:

git pull
easy_install virtualenv
easy_install pip
pip install -r polinax/requirements/external_apps.txt 

Things should just work out of the box. You can cd into project/polinax and
run ./manage.py syncdb and ./manage.py runserver to get running immediately.
