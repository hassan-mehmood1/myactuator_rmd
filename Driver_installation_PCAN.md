# PEAK PCAN-USB Module
I have tested with Peak PCAN-USB opto-decoupled IPEH-002022 (https://www.peak-system.com/PCAN-USB.199.0.html?L=1).
We do not need to install the driver since PCAN Module comes with default linux socket-can driver (https://python-can.readthedocs.io/en/stable/interfaces/pcan.html) which is required for RMD X series motor API.
In order to setup can0 we can use following commands(https://python-can.readthedocs.io/en/stable/interfaces/socketcan.html):
```bash
sudo ip link set can0 up type can bitrate 1000000
```

To check the CAN communication we can use following commands: 
Terminal1:
```bash
cansend can0 001#0000112200000000

```
Terminal2:
```bash
candump can0 

```

## 0. Overview
This repository holds a **CAN driver software development kit** (SDK) for the [**MyActuator RMD X actuator series**](https://www.myactuator.com/rmd-x) written in modern C++17 using [Linux's SocketCAN](https://docs.kernel.org/networking/can.html). The driver SDK is also exposed to Python through Python bindings generated with [pybind11](https://github.com/pybind/pybind11).

For the [`ros2_control` integration](https://control.ros.org/humble/index.html) please refer to [this repository](https://github.com/2b-t/myactuator_rmd_ros).



## 1. Installation

This driver SDK requires the **following dependencies** to be installed. For Debian Linux they can be installed through `apt` as follows:

```bash
$ sudo apt-get install -y build-essential cmake
$ sudo apt-get install -y can-utils iproute2 linux-modules-extra-$(uname -r)
```

In case you want to use the Python bindings you will have to additionally install [Python 3](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/) and [pybind11](https://pybind11.readthedocs.io/en/stable/):

```bash
$ sudo apt-get install -y python3 python3-pip python3-pybind11 python3-setuptools
```

After having installed its dependencies you will have to install the driver SDK either as a C++ library or Python package as described in the following steps. Both will use CMake to compile the C++ code.



### 1.1 Building the C++ library and Installing Python package

Before building C++ or python library makesure that you have cmake>3.20. You can check cmake version by using following commands:
```bash
cmake --version
# should be >= 3.20
```
If cmake is version is below 3.20 then you need to install it by using following commands:
```bash
sudo apt update
sudo apt install -y ca-certificates gnupg software-properties-common wget

# Add Kitware repository key + repo
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | \
  gpg --dearmor | sudo tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main" | \
  sudo tee /etc/apt/sources.list.d/kitware.list

sudo apt update
sudo apt install -y cmake
```
verify again:
```bash
cmake --version
# should be >= 3.20
```
Then you need to build it by using following commands:
```bash
cd ~/myactuator_rmd
rm -rf build
mkdir build
cd build

cmake .. \
  -D PYTHON_BINDINGS=on \
  -D CMAKE_CXX_STANDARD=17 \
  -D CMAKE_CXX_STANDARD_REQUIRED=ON \
  -D CMAKE_POLICY_VERSION_MINIMUM=3.5

cmake --build . -j$(nproc)

cd ~/myactuator_rmd

CMAKE_ARGS="-DCMAKE_CXX_STANDARD=17 -DCMAKE_POLICY_VERSION_MINIMUM=3.5" pip3 install .

echo 'export PYTHONPATH=$PYTHONPATH:~/myactuator_rmd/build' >> ~/.bashrc

```

Reboot
```bash
sudo reboot
```

For uninstalling the package again you can use [the following command](https://gitlab.kitware.com/cmake/community/-/wikis/FAQ#can-i-do-make-uninstall-with-cmake) `$ xargs rm < install_manifest.txt`.


If you want to remove them again simply invoke `$ pip3 uninstall myactuator-rmd-py`.


## 2. Using the C++ library

In case Ament is installed on your system but you want to install the package with CMake only, please make sure that your ROS 2 workspace was not sourced before running the installation.

In your CMake package you can then find the package and link to it as follows:

```cmake
cmake_minimum_required(VERSION 3.20)
project(your_project)

find_package(myactuator_rmd REQUIRED)

add_executable(your_node
  src/main.cpp
)
target_compile_features(your_node PUBLIC
  cxx_std_17
)
target_link_libraries(your_node PUBLIC
  myactuator_rmd::myactuator_rmd
)
```

A minimal example for the `main.cpp` can be found below:

```c++
#include <cstdlib>
#include <iostream>

#include <myactuator_rmd/myactuator_rmd.hpp>


int main() {
  myactuator_rmd::CanDriver driver {"can0"};
  myactuator_rmd::ActuatorInterface actuator {driver, 1};

  std::cout << actuator.getVersionDate() << std::endl;
  std::cout << actuator.sendPositionAbsoluteSetpoint(180.0, 500.0) << std::endl;
  actuator.shutdownMotor();
  return EXIT_SUCCESS;
}
```



## 3. Using the Python bindings

**Load the library** and continue to create a driver for a particular network interface (here `can0`) and drive (here `1` corresponding to the CAN-address `0x140 + 1 = 0x141`) and control it through the Python API as shown below:

```bash
$ python3
Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import myactuator_rmd_py as rmd
>>> driver = rmd.CanDriver("can0")
>>> actuator = rmd.ActuatorInterface(driver, 1)
>>> actuator.getVersionDate()
2023020601
>>> actuator.sendPositionAbsoluteSetpoint(180.0, 500.0)
temperature: 19, current: 0.1, shaft speed: 1, shaft angle: 0
>>> actuator.shutdownMotor()
```

In case you installed the package through ROS 2 the shared library will be located inside the `myactuator_rmd` package. Therefore you will need to import it with `import myactuator_rmd.myactuator_rmd_py as rmd`.

For more information you might also inspect the contents of the module inside Python 3 with `help(myactuator_rmd_py)`.



## 4. Automated tests

For testing you will have to install the following additional dependencies

```bash
$ sudo apt-get install -y libboost-all-dev libgmock-dev libgtest-dev
```

The tests can then be build by passing the **additional flag `-D BUILD_TESTING=on`** to CMake. After building the driver SDK with the additional flag you will have to bring the virtual CAN interface up with:

```bash
$ sudo modprobe vcan
$ sudo ip link add dev vcan_test type vcan
$ sudo ip link set up vcan_test
```

Additionally there is a CMake flag `SETUP_TEST_IFNAME` that - if set to `on` - automatically sets up the virtual CAN interface for you but this requires the following command to be run as `sudo`. Finally for coverage reports with GCC you might use the flag `ENABLE_COVERAGE` but this will compile the code without optimizations.

Finally you can **launch all the tests** with the following command:

```bash
$ ctest
```
