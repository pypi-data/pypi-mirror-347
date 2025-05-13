from setuptools import setup, find_packages

setup(
    name="uc_nsx_vmc_aws_integration_python_sdk",
    version="4.1.2.0.1",
    description="NSX VMC AWS INTEGRATION Python SDK",
    long_description="NSX VMC AWS INTEGRATION Policy APIs",
    long_description_content_type="text/markdown",
    author="VMware",
    author_email="support@vmware.com",
    url="https://github.com/vmware/vsphere-automation-sdk-python",
    packages=find_packages(),  # Automatically find all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # Add dependencies if required
)