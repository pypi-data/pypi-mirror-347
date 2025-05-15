from setuptools import setup, find_packages

setup(
    name='khmernames',
    version='0.7',
    packages=find_packages(),
    install_requires=[],
    author='Dev by Sammy KH',
    author_email='sammytoolsvplus@gmail.com',
    description='Pro version: Generate unlimited Khmer names without duplicates',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sammykh/khmernames',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='khmer names generator unlimited no-duplicate',
)
