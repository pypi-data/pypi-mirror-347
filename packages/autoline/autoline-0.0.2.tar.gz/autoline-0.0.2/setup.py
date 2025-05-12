import setuptools
# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()
install_requires=["pyautogui","pygetwindow","pyperclip"]
setuptools.setup(
    name = "autoline",
    version = " 0.0.2",
    author = "KuoYuanLi",
    author_email="funny4875@gmail.com",
    description="send line message automatically",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/autoline/",                                         packages=setuptools.find_packages(),     
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    )