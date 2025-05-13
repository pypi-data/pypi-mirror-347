import os
import sys
import subprocess
from pathlib import Path
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Windows-specific CMake configurations
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())

class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)
        extdir = ext_fullpath.parent.resolve()

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}{os.sep}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            # Windows-specific settings
            "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE",
            "-DBUILD_SHARED_LIBS=TRUE",
        ]

        build_args = []
        
        # Windows MSVC specific configuration
        #if sys.platform == "win32":
           # cmake_args += [
            #    "-A", PLAT_TO_CMAKE[self.plat_name],
            #    "-T", "host=x64"  # Use 64-bit toolchain
           #]
            #build_args += ["--config", cfg]

        # Except MSVC
        if sys.platform == "win32":
            cmake_args += [
                "-G", "Ninja", 
                # "-DCMAKE_MAKE_PROGRAM=ninja", 
            ]
            build_args += []
            

        # Handle additional CMake arguments
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        # Set build directory and ensure it exists
        build_temp = Path(self.build_temp) / ext.name
        if not build_temp.exists():
            build_temp.mkdir(parents=True)

        # Configure CMake
        subprocess.run(
            ["cmake", ext.sourcedir, *cmake_args], 
            cwd=build_temp, 
            check=True
        )
        
        # Build with CMake
        subprocess.run(
            ["cmake", "--build", ".", *build_args], 
            cwd=build_temp, 
            check=True
        )

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="PyRocketSim",
    version="0.2.3",
    author="Vladimir",
    description="Simulator dynamic flight rocket",
    ext_modules=[CMakeExtension("._rocketSim")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    install_requires=["matplotlib", "numpy"],
    python_requires=">=3.13",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown", 
)