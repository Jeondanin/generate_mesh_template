# GENERATE_MESH_TEMPLATE Project

This project is a C++ project using CMake and including the Armadillo library.

## Requirements

- CMake 3.27.9 or higher
- Windows OS: vcpkg
- Mac OS: only brew needed.
- Armadillo library
   - windows : vcpkg install armadillo
   - MacOS: brew install armadillo

## Build Instructions

1. Navigate to the project directory.
2. Create a build directory by running the following command:
   ```bash
   mkdir build
   cd build
   ```
3. Generate the build script using CMake:

- Windows (In case of vcpkg path="C:\src\vcpkg")
   ```bash
   cmake -DCMAKE_TOOLCHAIN_FILE=C:\src\vcpkg\scripts\buildsystems\vcpkg.cmake ..
   ```

- MacOS(Clang++ Compiler)
   ```bash
   cmake ..
   ```


4. Finish
- You have GENERATE_MESH_TEMPLATE.sln in `/build` directory and Load project using Visual Studio(Windows)
- You have Makefile in `/build` directory and You should `make`command to get a.out being compiled
   ```bash
   make
   ```
