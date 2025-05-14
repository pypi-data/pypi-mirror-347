from setuptools import setup, find_packages

setup(
    name='khmernames',
    version='0.3',
    packages=find_packages(),
    install_requires=[],  # No external dependencies needed for now
    author='Sammy KH',
    author_email='sammytoolsvplus@gmail.com',
    description='Generate random Khmer names for your projects',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sammykh/khmernames',  # ✅ update to real repo if available
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='khmer names generator random name-library khmer-language',
)
