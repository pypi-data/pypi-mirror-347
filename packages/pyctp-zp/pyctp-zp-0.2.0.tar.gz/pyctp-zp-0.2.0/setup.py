from setuptools import setup, find_packages
from setuptools.dist import Distribution
import os

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(('.pyd', '.dll', '.py')):
                paths.append(os.path.relpath(os.path.join(path, filename), directory))
    return paths

pyctp_files = package_files('PyCTP')
cppyctp_files = package_files('CPPyCTP')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyctp-zp',
    version='0.2.0',
    description='CTP Python接口（基于SWIG和C++官方API）',
    author='luochenyeling',
    author_email='zhaokehan86@163.com',
    packages=['PyCTP', 'CPPyCTP'],
    package_data={
        'PyCTP': pyctp_files,
        'CPPyCTP': cppyctp_files,
    },
    include_package_data=True,
    distclass=BinaryDistribution,
    zip_safe=False,
    python_requires='>=3.12',
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)