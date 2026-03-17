from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'keyboard_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=['keyboard_control'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='neo',
    maintainer_email='neo@example.com',
    description='Keyboard and GUI control for robot velocity commands',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_control_node = keyboard_control.keyboard_control_node:main',
        ],
    },
)