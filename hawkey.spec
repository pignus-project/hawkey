%global libsolv_version 0.6.4-1

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           hawkey
Version:        0.6.3
Release:        4%{?dist}
Summary:        Library providing simplified C and Python API to libsolv
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

Patch0001:      0001-sack-don-t-raise-error-when-non-existing-arch-is-use.patch
Patch0002:      0002-Fixes-for-building-with-libsolv-0.6.21-117.patch

BuildRequires:  libsolv-devel >= %{libsolv_version}
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  expat-devel
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel
BuildRequires:  check-devel
%ifnarch s390
BuildRequires:  valgrind
%endif
Requires:       libsolv%{?_isa} >= %{libsolv_version}

%description
A Library providing simplified C and Python API to libsolv.

%package devel
Summary:        A Library providing simplified C and Python API to libsolv
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel

%description devel
Development files for hawkey.

%package -n python2-%{name}
Summary:        Python 2 bindings for the hawkey library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires:  python2-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-nose
%else
BuildRequires:  python2-nose
%endif
%if (0%{?rhel} && 0%{?rhel} <= 7) || (0%{?fedora} && 0%{?fedora} <= 23)
BuildRequires:  python-sphinx
%else
BuildRequires:  python2-sphinx
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python2-%{name}
Python 2 bindings for the hawkey library.

%if %{with python3}
%package -n python3-%{name}
Summary:        Python 3 bindings for the hawkey library
%{?system_python_abi}
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the hawkey library.
%endif

%prep
%autosetup -p1

mkdir build

%if %{with python3}
mkdir build-py3
%endif

%build
pushd build
  %cmake ../
  %make_build
  make doc-man
popd

%if %{with python3}
pushd build-py3
  %cmake ../ -DPYTHON_DESIRED:str=3
  %make_build
  make doc-man
popd
%endif

%install
pushd build
  %make_install
popd
%if %{with python3}
pushd build-py3
  %make_install
popd
%endif

%check
if [ "$(id -u)" == "0" ] ; then
        cat <<ERROR 1>&2
Package tests cannot be run under superuser account.
Please build the package as non-root user.
ERROR
        exit 1
fi
pushd build
  ctest -VV
popd
%if %{with python3}
# Run just the Python tests, not all of them, since
# we have coverage of the core from the first build
pushd build-py3/tests/python
  ctest -VV
popd
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README.rst
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/
%{_mandir}/man3/%{name}.3*

%files -n python2-%{name}
%{python2_sitearch}/%{name}/

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%endif

%changelog
* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.3-4
- Add %%{?system_python_abi}
- Trim changelog

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 29 2016 Igor Gnatenko <ignatenko@redhat.com> 0.6.3-2
- spec: Fix packaging to comply packaging guidelines (Igor Gnatenko)
