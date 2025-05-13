from setuptools import setup, find_packages

setup(
    name='monkez_qwidgets',
    version='0.1.0',
    author='Monkez',
    author_email='tiendelai@gmail.com',
    description='My custom PyQt widgets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['opencv-python',
                      'PyQt-Fluent-Widgets[full]'
                      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
