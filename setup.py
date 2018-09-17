# _*_ coding: UTF-9 _*_

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='genosha',
    description="Mutant Homeland and a disaster zone.",
    long_description=readme(),
    keywords='test, mutations, subsuming, dominant',
    version='0.0.0',
    url='https://github.com/marcioaug/genosha',
    author='Marcio Augusto Guimarães',
    autho_email="masg@ic.ufal.br",
    license='MIT',
    package=['genosha', 'genosha.tools'],
    install_requires=[
        'hunor==0.2.0'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['genosha=genosha.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Test :: Mutation :: Subsuming'
    ]
)
