import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-pablo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A mediocre django fixture generator',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://prdpx7.github.io/',
    author='Pradeep Khileri',
    author_email='pradeepchoudhary009@gmail.com',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "Faker==6.5.0",
        "Django>=2.2"
    ],
)