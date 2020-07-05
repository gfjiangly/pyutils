# -*- encoding:utf-8 -*-
# @Time    : 2019/7/6 18:31
# @Author  : gfjiang
# @Site    : 
# @File    : setup.py
# @Software: PyCharm
from setuptools import find_packages, setup
from io import open


install_requires = [
    'numpy>=1.11.1',
    'opencv-python',
    'pillow',
    'matplotlib',
    'tqdm',
    'flask',
    'requests'
]


def readme():
    # PyPi默认支持的是rst格式描述，需添加type指定md格式(setup.cfg)
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def get_version():
    version_file = 'pyutils/version.py'
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='pyutilss',
    version=get_version(),
    description='Python Foundation Utilities',
    long_description=readme(),
    keywords='tools',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    # metadata for upload to PyPI
    author='Guangfeng Jiang',
    author_email='gfjiang_xxjl@163.com',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=install_requires,
    zip_safe=False,
)
