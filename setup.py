from setuptools import setup, find_packages

setup(
    name='AccessibilityTool',
    version='0.1.0',
    author='Felipe Murguia Leal',
    author_email='murguialeal@pm.me',
    description='Herramienta de accesibilidad para personas con discapacidad visual',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/v1persoul/AccessibilityTool',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "Flask",
        "pytest"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)