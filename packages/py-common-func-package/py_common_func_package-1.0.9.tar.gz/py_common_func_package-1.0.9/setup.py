from setuptools import setup, find_packages
# import platform

# 判断系统，自动选择编译后缀
# ext = ".pyd" if platform.system() == "Windows" else ".so"

setup(
    name="py_common_func_package",
    version="1.0.9",
    description = "python test common function",
    packages=['test_common'],  # 修改为你实际的包名
    package_dir={'test_common': 'obf'},
    # packages=find_packages(where='dist'),
    package_data={  # 确保混淆后的文件被包含
        'test_common':[
            'src/common_fun/*',
            'src/test_steps/*',
        ]
    },
    include_package_data=True,  # 确保包含 package_data 中的文件
    zip_safe=False,
    install_requires=[  # 如果有依赖的其他包
    ],
)
