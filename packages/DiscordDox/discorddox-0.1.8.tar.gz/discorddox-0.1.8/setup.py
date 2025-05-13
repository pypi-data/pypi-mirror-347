from setuptools import setup, find_packages

setup(
    name='DiscordDox',
    version='0.1.8',
    description='none',
    author='none',
    author_email='none@gmail.com',
    packages=find_packages(include=['DiscordDox', 'DiscordDox.*']),
    include_package_data=True,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'DiscordDox=DiscordDox.app:start_app'
        ]
    }
)
