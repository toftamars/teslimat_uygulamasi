from setuptools import setup, find_packages

setup(
    name='teslimat_uygulamasi',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'odoo>=16.0',
    ],
    author='Your Company',
    author_email='info@yourcompany.com',
    description='Teslimat planlama ve takip uygulamasi',
    keywords='odoo, teslimat, delivery',
    python_requires='>=3.8',
) 