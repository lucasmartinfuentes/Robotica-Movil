from glob import glob

from setuptools import find_packages, setup

package_name = 'lab2_rm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*')),
        ('share/' + package_name + '/config', glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lucas',
    maintainer_email='lucasmartinfuentes23@gmail.com',
    description='Lab 2 IIC2685: control en lazo cerrado y comportamientos reactivos',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'detector_de_objeto = lab2_rm.detector_de_objeto:main',
            'seguidor_de_objeto = lab2_rm.seguidor_de_objeto:main',
            'lazo_cerrado_nav = lab2_rm.lazo_cerrado_nav:main',
            'pose_loader = lab2_rm.pose_loader:main',
            'pose_recorder = lab2_rm.pose_recorder:main',
        ],
    },
)
