import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RxnIM",                   # 模块名称
    version="1.0",                  # 当前版本
    author="CHEN Yufan",            # 作者
    author_email="ychenkv@connect.ust.hk",
    description="RxnIM",            # 模块简介



    license="MIT",                  # SPDX 短标识符
    license_file="LICENSE.txt",     # 指向你的许可证文件

    packages=setuptools.find_packages(),
    include_package_data=True,      # 必须配合 MANIFEST.in
    package_data={
        "": ["*.pth"],
    },
    install_requires=[
        "torch",
        "numpy>=1.19.5",
        "pandas>=1.2.4",
        "Pillow==9.5.0",
        "matplotlib>=3.5.3",
        "opencv-python>=4.5.5.64",
        "pycocotools>=2.0.4",
        "pytorch-lightning>=1.8.6",
        "transformers>=4.5.1",
        "huggingface-hub>=0.11.0",
        "MolScribe",
        "easyocr>=1.6.2",
    ],

    python_requires="==3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
