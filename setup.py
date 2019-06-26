import setuptools
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

test_reqs = parse_requirements('dev-requirements.txt', session='hack')
dev_reqs = [str(ir.req) for ir in test_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('version.py','r') as fp:
  globals_dict = {}
  exec(fp.read(), globals_dict)  # pylint: disable=exec-used
__version__ = globals_dict['__version__']

setuptools.setup(
    name="nlp_gcp",
    version=__version__,
    author="Renault Digital Datascience Team",
    author_email="data-sciences@renault.com",
    description="TFX based ML model tf-sample-model",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="",
    packages=setuptools.find_packages(),
    package_data={'': ['requirements.txt', 'README.md']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Data Scientists',
        'Topic :: Scientific/Engineering :: Machine Learning',
    ],
    install_requires=reqs,
    setup_requires=[
        'pytest-runner'
    ],
    include_package_data=True,
    zip_safe=True,
    tests_require = dev_reqs,
)