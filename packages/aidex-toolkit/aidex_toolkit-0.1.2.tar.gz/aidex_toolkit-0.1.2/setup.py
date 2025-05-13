from setuptools import setup, find_packages

setup(
    name='aidex_toolkit',
     version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    entry_points={
        "console_scripts": [
            "aidex_toolkit=aidex_toolkit.__main__:main",
        ],
    },
    include_package_data=True,
    author='Godsave Kawurem',
    author_email='godsaveogbidor@gmail.com',
    description='Ai/ML trainings package and guide from scratch with sample data support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Perfect-Aimers-Enterprise/aidex_toolkit.git',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
