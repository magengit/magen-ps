from setuptools import setup
import sys
import pip

if sys.version_info < (3, 5, 2):
    sys.exit("Sorry, you need Python 3.5.2+")

pip_version = int(pip.__version__.replace(".", ""))
if pip_version < 901:
        sys.exit("Sorry, you need pip 9.0.1+")

setup(
    name='magen_location_service',
    version='1.0a2',
    install_requires=[
        'aniso8601>=1.2.1',
        'consulate>=0.6.0',
        'coverage>=4.4.1',
        'flake8>=3.3.0',
        'Flask>=0.12.2',
        'Flask-Cors>=3.0.3',
        'pycrypto>=2.6.1',
        'pymongo>=3.4.0',
        'pytest>=3.1.3',
        'requests>=2.13.0',
        'responses>=0.5.1',
        'Sphinx>=1.6.3',
        'wheel>=0.30.0a0',
        'magen_logger==1.0a1',
        'magen_utils==1.2a2',
        'magen_test_utils==1.0a1',
        'magen_mongo==1.0a1',
        'magen_rest_service==1.0a1',
        'magen_statistics_service==1.0a1'
      ],
    scripts=['location_server/location_server.py'],
    package_dir={'': '..'},
    packages={
        # 'magen_location/docs/_build/html', # chicken-and-egg problem building docs
        'magen_location', 'magen_location.location_client',
        'magen_location.location_server', 'magen_location.location_libs',
        'magen_location.location_apis',
        'magen_dctx', 'magen_dctx.dctx_agt_server', 
        'magen_dctx.dctx_lib', 'magen_dctx.dctx_agt_apis',
        'magen_dctx.mongo_dctx'
    },
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.html']
    },
    # test_suite='tests',
    url='',
    license='Proprietary License',
    author='Alena Lifar',
    author_email='alifar@cisco.com',
    description='Location MicroService Package',
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
