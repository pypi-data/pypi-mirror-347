from setuptools import setup, find_packages

setup(
    name='TrackAlpaca',  # Name of the package
    version='0.1',  # Package version
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[  # List of dependencies
        'matplotlib', 
        'pillow'
    ],
    description='A Metric Tracking and Visualization Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Raziel Moesch',  # Your name
    author_email='razielmoeschwork@gmail.com',  # Your email
    url='https://github.com/RazielMoesch/TrackAlpaca',  # URL of the project
    classifiers=[  # Classifiers to categorize the project
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Python version compatibility
)
