from setuptools import setup, Extension
import platform

system = platform.system()
extra_compile_args = ["-std=c++17"]
include_dirs = ["GladUI/include", "GladUI/assets/GladG"]
libraries = []
library_dirs = []
extra_link_args = []

if system == "Windows":
    libraries = ["SDL2", "SDL2_ttf", "SDL2_image", "SDL2_mixer"]
    library_dirs = ["GladUI/lib/windows"]
elif system in ["Linux", "Darwin"]:
    libraries = ["SDL2", "SDL2_ttf", "SDL2_image", "SDL2_mixer"]

GladUI_ext = Extension(
    "GladUI.GladUI",  # Note this! 'GladUI' package and native module 'GladUI.so'
    sources=["GladUI/GladUI.cpp"],
    include_dirs=include_dirs,
    libraries=libraries,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c++"
)

setup(
    name="GladUI",
    version="0.1.0",
    description="Cross-platform C++ GUI engine using SDL2",
    license = "MIT",
    author="Navthej",
    packages=["GladUI"],
    package_data={
        "GladUI": [
            "lib/windows/*.dll",
            "include/SDL2/*.h",
            "assets/GladG/*.h",
        ]
    },
    include_package_data=True,
    ext_modules=[GladUI_ext],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    )
