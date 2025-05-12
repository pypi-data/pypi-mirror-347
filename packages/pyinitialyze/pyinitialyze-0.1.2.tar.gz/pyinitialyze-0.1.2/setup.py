from setuptools import setup, find_packages

setup(
    name='pyinitialyze',
    version='0.1.2',
    description='A Python lib you can use to initialize your Python scripts (Console based / Windowed)',
    author='Guillaume Plagier',
    packages=find_packages(),
    package_data={
        'pyinitialyze': ['Dll/win32dll.exe']
    },
)
