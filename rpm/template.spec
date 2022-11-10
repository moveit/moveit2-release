%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-moveit-resources-prbt-moveit-config
Version:        2.6.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_resources_prbt_moveit_config package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-joint-state-publisher
Requires:       ros-rolling-moveit-resources-prbt-ikfast-manipulator-plugin
Requires:       ros-rolling-moveit-resources-prbt-support
Requires:       ros-rolling-moveit-ros-move-group
Requires:       ros-rolling-robot-state-publisher
Requires:       ros-rolling-rviz2
Requires:       ros-rolling-xacro
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
MoveIt Resources for testing: Pilz PRBT 6 A project-internal configuration for
testing in MoveIt.

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
* Thu Nov 10 2022 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 2.6.0-1
- Autogenerated by Bloom

* Thu Jul 28 2022 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 2.5.3-1
- Autogenerated by Bloom

* Mon Jul 25 2022 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 2.5.2-1
- Autogenerated by Bloom

* Wed Jun 01 2022 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 2.5.1-1
- Autogenerated by Bloom

* Thu May 26 2022 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 2.5.0-1
- Autogenerated by Bloom
