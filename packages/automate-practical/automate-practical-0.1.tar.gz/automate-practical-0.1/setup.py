from setuptools import setup,find_packages

setup(
    name='automate-practical',
    version='0.1',
    packages=find_packages(), 
    include_package_data=True, 
    description='My automation tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)