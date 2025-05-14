from setuptools import setup, find_packages

setup(
    name='VDP',
    version='0.1.0',
    author='Rohaan Nadeem',
    author_email='rohaan.nadeem@fulbrightmail.org',
    description='Variational Density Propagation (VDP) CNN Layers for TensorFlow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dimahdera/PremiUm-CNN-CIFAR10-Tensorflow-2.x',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'numpy',
        'matplotlib',
        'pandas',
        'scipy',
        'xlsxwriter',
        'wandb'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)