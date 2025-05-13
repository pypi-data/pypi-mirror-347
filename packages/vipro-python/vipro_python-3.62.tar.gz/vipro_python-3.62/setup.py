from setuptools import setup, find_packages

PACKAGE_VERSION="3.62"

setup(
    name='vipro_python',
    version=PACKAGE_VERSION,
    license='MIT',
    description='A set of convenience functions to make writing python, mostly in jupyter notebooks, as efficient as possible.',
    long_description='A set of convenience functions to make writing python, mostly in jupyter notebooks, as efficient as possible.',
    author="Tom Medhurst",
    author_email='tom.medhurst@vigilantapps.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/underpinning/vipro-python',
    keywords='vipro jupyter jupyterlab notebook pika amqp convenience',
    install_requires=[
      'pika',
      'twine',
      'pandas',
      'numpy',
      'nameparser',
      'jellyfish',
      'google-cloud-storage',
      'google-cloud-firestore',
      'google-cloud-pubsub',
      'google-cloud-secret-manager',
      'cloudevents',
      'tensorflow',
      'requests',
      'openpyxl',
      'xlrd',
    ],
)