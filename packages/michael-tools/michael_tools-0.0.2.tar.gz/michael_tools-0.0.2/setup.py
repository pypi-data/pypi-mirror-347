from setuptools import setup, find_packages

setup(
    name='michael_tools',
    version='0.0.2',
    author='Michael Smith',
    author_email='1422749310@qq.com',
    description='This is my personal toolkit',
    packages=find_packages(),  # 自动发现所有模块

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    install_requires=[  # 依赖项（可选）
        # 'requests',
    ],
)
