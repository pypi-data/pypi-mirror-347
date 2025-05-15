from setuptools import setup, find_packages

setup(
    name='automata_practical_exam',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[  
        'pytest'
    ],
    test_suite='tests',  
    author='Mohamed Fathy',
    author_email='moham6dfathy@gmail.com',
    description='A description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Moham6dFathy/automata_practical_exam_4552',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)