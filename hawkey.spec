%global gitrev afa7717
%global libsolv_version 0.0.0-17

Name:		hawkey
Version:	0.3.0
Release:	1.git%{gitrev}%{?dist}
Summary:	Library providing simplified C and Python API to libsolv
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		https://github.com/akozumpl/hawkey
# git clone https://github.com/akozumpl/hawkey.git && cd hawkey && package/archive
Source0:	hawkey-%{gitrev}.tar.xz
BuildRequires:	libsolv-devel >= %{libsolv_version}
BuildRequires:	cmake expat-devel rpm-devel zlib-devel check-devel
BuildRequires:	python2-devel
BuildRequires:	python-nose
BuildRequires:	python-sphinx
# explicit dependency: libsolv occasionally goes through ABI changes without
# bumping the .so number:
Requires:	libsolv%{?_isa} >= %{libsolv_version}

# prevent provides from nonstandard paths:
%filter_provides_in %{python_sitearch}/.*\.so$
# filter out _hawkey_testmodule.so DT_NEEDED _hawkeymodule.so:
%filter_requires_in %{python_sitearch}/hawkey/test/.*\.so$
%filter_setup

%description
A Library providing simplified C and Python API to libsolv.

%package devel
Summary:	A Library providing simplified C and Python API to libsolv
Group:		Development/Libraries
Requires:	hawkey%{?_isa} = %{version}-%{release}

%description devel
Development files for hawkey.

%package -n python-hawkey
Summary:	Python bindings for the hawkey library
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python-hawkey
Python bindings for the hawkey library.

%prep
%setup -q -n hawkey

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make %{?_smp_mflags}
make doc-man

%check
make ARGS="-V" test

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README.md
%{_libdir}/libhawkey.so.*

%files devel
%{_libdir}/libhawkey.so
%{_libdir}/pkgconfig/hawkey.pc
%{_includedir}/hawkey/
%{_mandir}/man3/hawkey.3.gz

%files -n python-hawkey
%{python_sitearch}/

%changelog
* Fri Oct 5 2012 Aleš Kozumplík <ales@redhat.com> - 0.2.12-2.git7fa7aa9
- fix sigsegv in query.c:filter_sourcerpm().
- doc: move the hawkey reference to man section 3.
- query: filter by description or URL.
- fix: FOR_PACKAGELIST(pkg,list,i) offsets the 'i' by one.
- Query: hy_query_filter_package_in() limits filtering to an arbitrary set of pkgs.
- Query: filtering by epoch.
- py: Query: make sure filterm() clears the result cache.
- py: fix: memory leaks with PySequence_GetItem().

* Mon Sep 22 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.11-4.git687ceab
- py: hawkey.test should not depend on libcheck.so.

* Fri Sep 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.11-1.git545a461
- py: Goal.run_all() returns True if a solution was found. (RhBug: 856615)
- py: Goal.run() accepts callback parameter too. (RhBug: 856615)
- query: filtering by version and release. (RhBug: 856612)
- Flag an error if Sack is created with an invalid arch. (RhBug: 857944)
- fix hy_get_sourcerpm() when the package has no sourcerpm. (RhBug: 858207)
- Query: filter by source rpm. (RhBug: 857941)
- Run 'make check' when building the RPM.

* Mon Sep 10 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.10-2.gita198dea
- Fix build that now needs python-sphinx.

* Thu Aug 30 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.10-1.gita198dea
- Query cloning.
- Query: full version filtery is supported now.
- py: query.filter() now returns a cloned Query.
- py: len(query) and bool(query) now work as expected.

* Thu Aug 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.9-2.gitefeb04c
- Add manpage.

* Thu Aug 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.9-1.git8599c55
- Finding all solutions in Goal.
- hy_goal_reason() no longer depends on Fedora-specific hacks in libsolv.
- hy_package_get_sourcerpm()

* Mon Aug 6 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.8-1.gite6734fb
- repo loading API changed, hy_sack_load_yum_repo() now accepts flags to build
  cache, load filelists, etc.
- fixed 843487: hawkey query.filter() ends with assertion.

* Tue Jul 24 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.7-1.git41b39ba
- Package description, license, url support.
- python: Unicode fixes in Query.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-3.gitea88ad5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-2.gitea88ad5
- HY_CLEAN_DEPS support.

* Mon Jul 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.6-1.git76a5b8c
- Use libsolv-0.0.0-13.
- hy_goal_get_reason().

* Sun Jul 1 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.5-1.git042738b
- Use libsolv-0.0.0-12.
- Added hy_package_get_hdr_checkum().

* Mon Jun 25 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-8.git04ecf00
- More package review issues.

* Fri Jun 22 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-7.git04ecf00
- More package review issues.

* Wed Jun 20 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-6.git04ecf00
- Prevent requires in the hawkey.test .so.

* Tue Jun 19 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-5.git04ecf00
- Fix rpmlint issues.

* Wed Jun 13 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-4.git04ecf00{?dist}
- Downgrades.

* Fri Jun 8 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.4-2.git1f198aa{?dist}
- Handling presto metadata.

* Wed May 16 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.3-1.git6083b79{?dist}
- Support libsolv's SOLVER_FLAGS_ALLOW_UNINSTALL.

* Mon May 14 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.2-1.git46bc9ec{?dist}
- Api cleanups.

* Fri May 4 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.1-1.gita59de8c0{?dist}
- Goal.update() takes flags to skip checking a pkg is installed.

* Tue Apr 24 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.2.0-4.gita7fafb2%{?dist}
- hy_query_filter_in()
- Better unit test support.

* Thu Apr 12 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.1-6.git0e6805c%{?dist}
- Initial package.
