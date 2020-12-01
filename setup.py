from setuptools import setup
setup(
    name = 'booking-system',
    version = '0.1.0',
    packages = ['booking-system'],
    entry_points = {
        'console_scripts': [
            'booking_system = main:main'
        ]
    })
