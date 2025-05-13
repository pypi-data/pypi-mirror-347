from setuptools import setup, find_packages

setup(
    name='TelegramDoxing',
    version='0.1.0',
    description='none',
    author='none',
    author_email='none@gmail.com',
    packages=find_packages(include=['TelegramDoxing', 'TelegramDoxing.*']),
    include_package_data=True,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'TelegramDoxing=TelegramDoxing.app:start_app'
        ]
    }
)
