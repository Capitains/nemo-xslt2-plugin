from setuptools import setup, find_packages

setup(
    name='nemo_xslttwo_plugin',
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/capitains/nemo-xslt2-plugin',
    license='GNU GPL',
    author='Thibault Clerice',
    author_email='leponteineptique@gmail.com',
    description='Plugin for Capitains Nemo to transform XML through XSLT2 Jar of Saxon',
    test_suite="tests",
    tests_require=[
        "capitains_nautilus>=0.0.5",
        "flask_nemo>=1.0.0b2",
        "Werkzeug>=0.11.0"
    ],
    install_requires=[]
)
