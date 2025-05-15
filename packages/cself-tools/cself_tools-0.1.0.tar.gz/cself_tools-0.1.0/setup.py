from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cself_tools",
    version="0.1.0",
    author="WANGQinglin",
    author_email="chd_wql@qq.com",  # 替换为您的邮箱
    description="极低频视电阻率数据处理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chdwql/cself_tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cx_Oracle",
        "pandas",
        "numpy",
        "matplotlib",
        "addereq",  # 如果这是私有包，可能需要特殊处理
    ],
    entry_points={
        'console_scripts': [
            'cself=cself_tools.cli:main',
        ],
    },
)
