from setuptools import setup

setup(
    name="foyeshow",
    version="0.0.1",
    author="foye",
    author_email="845903926@qq.com",
    description="A small toy that replaces OpenCV's imshow combination with pure Python implementation",
    # 如果你的库只有一个 .py 文件，需要改用 py_modules 配置
    py_modules=["foyeshow"],  # 假设你的文件是 foyeshow.py
    install_requires=["numpy>=1.20.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",  # 修正分类器格式
    ],
    python_requires='>=3.11.4',
)