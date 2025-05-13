from setuptools import setup, find_packages

setup(
    name="uc_vmwarecloud_draas",
    version="1.23.0",
    description="uc_vmwarecloud_draas",
    long_description="uc_vmwarecloud_draas",
    long_description_content_type="text/markdown",
    author="VMware",
    author_email="support@vmware.com",
    url="https://github.com/vmware/vsphere-automation-sdk-python",
    packages=find_packages(include=["com*", "vmware*"]),  # Include specific top-level packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # Add dependencies if needed
)