from setuptools import setup, find_packages
import sys
import pip

if sys.version_info < (3, 5, 2):
    sys.exit("Sorry, you need Python 3.5.2+")

pip_version = int(pip.__version__.replace(".", ""))
if pip_version < 901:
        sys.exit("Sorry, you need pip 9.0.1+")

setup(
    name='magen_policy_service',
    version='1.0a1',
    install_requires=[
        'aniso8601>=1.2.1',
        'coverage>=4.4.1',
        'flake8>=3.3.0',
        'Flask>=0.12.2',
        'Flask-Cors>=3.0.3',
        'pymongo>=3.4.0',
        'pytest>=3.1.3',
        'requests>=2.13.0',
        'responses>=0.8.1',
        'Sphinx>=1.6.3',
        'wheel>=0.30.0a0',
        'googlemaps>=2.5.1',
        'magen_id_client>=1.1a1',
        'magen_logger>=1.0a1',
        'magen_mongo>=1.0a1',
        'magen_rest_service>=1.2a1',
        'magen_statistics_service>=1.0a1',
        'magen_utils>=1.2a2',
        'magen_location_service>=1.0a1'
      ],
    scripts=['policy_server/policy_server.py',
             '../policy_scripts/policy_server_wrapper.sh'],
    package_dir={'': '..'},
    packages={
        #'policy/docs/_build/html', # chicken-and-egg problem building docs
        'policy', 'policy.policy_server', 'policy.policy_libs',
        'policy.policy_apis', 'policy.mongo_apis', 'policy.google_maps_apis'
    },
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.html']
    },
    test_suite='tests',
    url='',
    license='',
    author='Reinaldo Penno',
    author_email='repenno@cisco.com',
    description='Policy Microservice Package',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Legal Industry',
        'Topic :: Security',

        # Pick your license as you wish (should match "license" above)
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
)
