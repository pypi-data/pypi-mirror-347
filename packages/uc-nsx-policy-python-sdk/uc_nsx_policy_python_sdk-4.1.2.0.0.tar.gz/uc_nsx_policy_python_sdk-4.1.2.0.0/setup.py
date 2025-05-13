from setuptools import setup, find_packages

setup(
    name="uc_nsx_policy_python_sdk",
    version="4.1.2.0.0",
    description="uc_nsx_policy_python_sdk",
    long_description="uc_nsx_policy_python_sdk",
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