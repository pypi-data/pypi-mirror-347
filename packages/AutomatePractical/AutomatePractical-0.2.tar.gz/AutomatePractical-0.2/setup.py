from setuptools import setup,find_packages

setup(
    name='AutomatePractical',
    version='0.2',
    packages=find_packages(), 
    include_package_data=True, 
    description='My automation tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)