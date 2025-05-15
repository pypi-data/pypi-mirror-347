from setuptools import setup, find_packages

setup(
    name='doublylist',  # must be globally unique on PyPI
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'doublylist': ['doublylist/bin/doubly.dll'],  # include DLL file
    },
    author='Erdal Nayir',
    author_email='erdal.nayir2001@gmail.com',
    description='Python wrapper for a C doubly linked list implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/YourUsername/doublylist',  # or any homepage
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.10',
    zip_safe=False,
)