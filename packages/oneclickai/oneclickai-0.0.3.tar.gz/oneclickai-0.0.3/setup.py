from setuptools import setup, find_packages

install_requires = [
    'ultralytics==8.3.28',
    'opencv-python==4.10.0.84',
    'tensorflow==2.11; python_version < "3.11"',
    'tensorflow==2.18; python_version >= "3.11"',
]

setup(
    name='oneclickai',
    version='0.0.3',
    description='OneclickAI package for learning AI with python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Seung Oh',
    author_email='osy044@naver.com',
    url='https://oneclickai.co.kr',
    install_requires=install_requires,
    packages=find_packages(exclude=[]),
    keywords=['oneclick', 'clickai', 'learning ai', 'ai model', 'ai', 'ai package', 'oneclickai', 'oneclickai package'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)