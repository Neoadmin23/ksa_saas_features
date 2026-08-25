from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

from ksa_saas_features import __version__ as version

setup(
    name="ksa_saas_features",
    version=version,
    description="SaaS Feature Gating & Saudi HR Government Integrations for Frappe",
    author="Your Company",
    author_email="dev@yourdomain.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
