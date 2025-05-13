from setuptools import setup, find_packages

setup(
    name='pyOASIS',
    version='1.0.0',
    author='Giorgio Picanço',
    author_email='giorgiopicanco@gmail.com',
    description='Open-Access System for Ionospheric Studies (OASIS)',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/giorgiopicanco/OASIS',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    python_requires='>=3.8',
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=True,
)
