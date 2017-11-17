from setuptools import setup, find_packages


with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]

try:
    import pypandoc
    from os import path
    here = path.abspath(path.dirname(__file__))
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst'),
except ImportError:
    long_description = ""

setup(
    name='scs_core',
    version='0.1.6',
    description='Core package for South Coast Science Software',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs_core',
    package_dir={'scs_core':'scs_core'},
    packages=find_packages('scs_core'),
    # packages=['scs_core'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # package_data=["requirements.txt"],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3",
    extras_require={
        'dev': [
            'pypandoc'
        ]
    }
)
   