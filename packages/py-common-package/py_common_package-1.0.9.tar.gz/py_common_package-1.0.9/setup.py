from setuptools import setup, find_packages
# import platform

# 判断系统，自动选择编译后缀
# ext = ".pyd" if platform.system() == "Windows" else ".so"

setup(
    name="py_common_package",
    version="1.0.9",
    description = "python test common function or case_step",
    author="wl11",
    author_email="wl_926454@163.com",
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    # package_data={
    #     'src':[
    #         'src/common_fun/*',
    #         'src/test_steps/*',
    #     ]
    # },
    include_package_data=True,  # 确保包含 package_data 中的文件
    zip_safe=False,
    install_requires=[  # 如果有依赖的其他包

    ],
)
