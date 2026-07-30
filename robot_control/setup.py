import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jeppe Hansen',
    maintainer_email='jeppha@mmmi.sdu.dk',
    description='Package for implementing control for the mobile robot',
    license='MIT',
    entry_points={
        'console_scripts': [
        ],
    },
)
