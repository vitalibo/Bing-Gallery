import setuptools

setuptools.setup(
    name='bing_gallery',
    version='0.4.0',
    author='Vitaliy Boyarsky',
    author_email='boyarsky.vitaliy@live.com',
    description='Command-line tool for change a desktop picture based on daily Bing images',
    url='https://github.com/vitalibo/bing-gallery',
    packages=[
        ''
    ],
    package_dir={
        '': 'src/main'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'bing_gallery=bing_gallery:main'
        ]
    }
)
