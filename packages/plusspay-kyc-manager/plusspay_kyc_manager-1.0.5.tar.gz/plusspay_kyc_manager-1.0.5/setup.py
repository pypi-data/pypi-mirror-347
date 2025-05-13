from setuptools import setup, find_packages

readme = open("./README.md", "r")

setup(
    name='plusspay_kyc_manager',
    #packages=['plusspay_kyc_manager'],  # this must be the same as the name above
    version='1.0.5',
    description='Librería de Plusspay© para la gestión de procesos KYC (Know Your Customer) a través de diferentes proveedores.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Plusspay',
    author_email='',
    # use the URL to the github repo
    url='https://github.com/Pluss-Pay/kyc-didi',
    download_url='https://github.com/Pluss-Pay/kyc-didi/tarball/1.0.5',
    keywords=['plusspay'],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    'requests',
	'python-dotenv',
	'httpx'
    ]
   
    
)
