from setuptools import find_packages, setup

setup(
    name='simplifykm',
    packages=find_packages(include=['Auto']),
    version='0.1.5',
    description='This library automates tasks.',
    author='Khemraj Mangal',
    install_requires=["pandas", "numpy", "scikit-learn"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)