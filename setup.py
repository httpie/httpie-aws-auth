from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-aws-auth',
    description='AWS/S3 auth plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.0.2',
    author='Jakub Roztocil',
    author_email='jakub@roztocil.co',
    license='BSD',
    url='https://github.com/jkbrzt/httpie-aws-auth',
    download_url='https://github.com/jkbrzt/httpie-aws-auth',
    py_modules=['httpie_aws_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_aws_auth = httpie_aws_auth:AWSAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.7',
        'requests-aws>=0.1.8'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
