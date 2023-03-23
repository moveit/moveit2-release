%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-moveit-core
Version:        2.7.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_core package

License:        BSD-3-Clause
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       assimp-devel
Requires:       boost-devel
Requires:       boost-python%{python3_pkgversion}-devel
Requires:       bullet-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       ros-rolling-angles
Requires:       ros-rolling-common-interfaces
Requires:       ros-rolling-eigen-stl-containers
Requires:       ros-rolling-eigen3-cmake-module
Requires:       ros-rolling-geometric-shapes
Requires:       ros-rolling-geometry-msgs
Requires:       ros-rolling-kdl-parser
Requires:       ros-rolling-moveit-common
Requires:       ros-rolling-moveit-msgs
Requires:       ros-rolling-octomap
Requires:       ros-rolling-octomap-msgs
Requires:       ros-rolling-pluginlib
Requires:       ros-rolling-pybind11-vendor
Requires:       ros-rolling-random-numbers
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-ruckig
Requires:       ros-rolling-sensor-msgs
Requires:       ros-rolling-shape-msgs
Requires:       ros-rolling-srdfdom
Requires:       ros-rolling-std-msgs
Requires:       ros-rolling-tf2
Requires:       ros-rolling-tf2-eigen
Requires:       ros-rolling-tf2-geometry-msgs
Requires:       ros-rolling-tf2-kdl
Requires:       ros-rolling-trajectory-msgs
Requires:       ros-rolling-urdf
Requires:       ros-rolling-urdfdom
Requires:       ros-rolling-urdfdom-headers
Requires:       ros-rolling-visualization-msgs
Requires:       ros-rolling-ros-workspace
BuildRequires:  assimp-devel
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  bullet-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-angles
BuildRequires:  ros-rolling-common-interfaces
BuildRequires:  ros-rolling-eigen-stl-containers
BuildRequires:  ros-rolling-eigen3-cmake-module
BuildRequires:  ros-rolling-geometric-shapes
BuildRequires:  ros-rolling-geometry-msgs
BuildRequires:  ros-rolling-kdl-parser
BuildRequires:  ros-rolling-moveit-common
BuildRequires:  ros-rolling-moveit-msgs
BuildRequires:  ros-rolling-octomap
BuildRequires:  ros-rolling-octomap-msgs
BuildRequires:  ros-rolling-pluginlib
BuildRequires:  ros-rolling-pybind11-vendor
BuildRequires:  ros-rolling-random-numbers
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-ruckig
BuildRequires:  ros-rolling-sensor-msgs
BuildRequires:  ros-rolling-shape-msgs
BuildRequires:  ros-rolling-srdfdom
BuildRequires:  ros-rolling-std-msgs
BuildRequires:  ros-rolling-tf2
BuildRequires:  ros-rolling-tf2-eigen
BuildRequires:  ros-rolling-tf2-geometry-msgs
BuildRequires:  ros-rolling-tf2-kdl
BuildRequires:  ros-rolling-trajectory-msgs
BuildRequires:  ros-rolling-urdf
BuildRequires:  ros-rolling-urdfdom
BuildRequires:  ros-rolling-urdfdom-headers
BuildRequires:  ros-rolling-visualization-msgs
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gmock
BuildRequires:  ros-rolling-ament-cmake-gtest
BuildRequires:  ros-rolling-ament-index-cpp
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
BuildRequires:  ros-rolling-moveit-resources-panda-moveit-config
BuildRequires:  ros-rolling-moveit-resources-pr2-description
BuildRequires:  ros-rolling-orocos-kdl-vendor
%endif

%description
Core libraries used by MoveIt

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Thu Mar 23 2023 Henning Kayser <henningkayser@picknik.ai> - 2.7.1-1
- Autogenerated by Bloom

* Tue Mar 21 2023 Henning Kayser <henningkayser@picknik.ai> - 2.7.0-2
- Autogenerated by Bloom

