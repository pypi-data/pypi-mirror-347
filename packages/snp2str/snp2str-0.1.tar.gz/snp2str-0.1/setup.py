from setuptools import setup, find_packages
import os


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()


# Use absolute path to requirements.txt
req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(req_path) as f:
    required = f.read().splitlines()

setup(name='snp2str',
      version='0.1',
      description='A Python tool for converting SNP genotype data in PED format to a format suitable for STRUCTURE analysis',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://github.com/vladgheorghe/snp2str',
      author='Vlad Gheorghe',
      author_email='vlad.datapro@gmail.com',
      license='MIT',
      packages=find_packages(),  # This will find snp2str and snp2str.tests
      scripts=['bin/snp2str'],
      install_requires=required,
      include_package_data=True,
      python_requires='>=3.6',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      zip_safe=False)
