from setuptools import find_packages, setup

package_name = 'vision_stack'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='v1ndicator',
    maintainer_email='v1ndictivev1ndicat0r@proton.me',
    description='Houses nodes for opencv functionality',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        	'image_publisher = vision_stack.image_publisher:main',
		'edge_recog = vision_stack.edge_recog:main',
		'bin_mask = vision_stack.bin_mask:main',
		'line_recog = vision_stack.line_recog:main'
	],
    },
)
