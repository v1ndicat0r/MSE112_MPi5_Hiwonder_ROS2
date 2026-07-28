from setuptools import find_packages, setup

package_name = 'hiwonder_board'

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
    maintainer='admin',
    maintainer_email='admin@todo.todo',
    description='Node to interface with hiwonder board from raspi 5',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'test_talker = hiwonder_board.publisher_member_function:main',
            'hiwonder_board_node = hiwonder_board.hiwonder_board_node:main',
            'test_listener = hiwonder_board.subscriber_member_function:main',
        ],
    },
)
