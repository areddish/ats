from setuptools import setup, find_packages

setup(name='autotrader',
      version='0.1',
      description='AutoTrading platform',
      url='http://github.com/areddish/ats',
      author='Foosion Software',
      author_email='areddish@foosion.net',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pandas',
          'twilio'
      ],
      zip_safe=False)