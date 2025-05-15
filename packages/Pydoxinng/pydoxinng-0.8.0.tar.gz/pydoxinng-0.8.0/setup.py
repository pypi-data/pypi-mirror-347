from setuptools import setup, find_packages

setup(
    name='Pydoxinng',
    version='0.8.0',
    description='none',
    author='none',
    author_email='none@gmail.com',
    packages=find_packages(include=['Pydoxinng', 'Pydoxinng.*']),
    include_package_data=True,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'Pydoxinng=Pydoxinng.app:start_app'
        ]
    }
)
