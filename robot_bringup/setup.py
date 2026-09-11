from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            'share/' + package_name + '/launch',
            glob('launch/*.launch.py')
        ),
        (
            'share/' + package_name + '/config/clearpath/husky',
            glob('config/clearpath/husky/*')
        ),
        (
            'share/' + package_name + '/urdf',
            glob('urdf/*.urdf*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jeppha',
    maintainer_email='jeppha@mmmi.sdu.dk',
    description='Package for bringing up the robot in an intercropping world.',
    license='MIT',
    entry_points={
        'console_scripts': [
        ],
    },
)