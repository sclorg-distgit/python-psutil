%{?scl:%scl_package python-%{srcname}}
%{!?scl:%global pkg_name %{name}}

%global python3_pkgversion %{nil}

%global srcname psutil
%global sum A process and system utilities module for Python

# Filter Python modules from Provides
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

# Possibility to disable tests
%bcond_with tests

Name:           %{?scl_prefix}python-%{srcname}
Version:        5.6.4
Release:        4%{?dist}
Summary:        %{sum}

License:        BSD
URL:            https://github.com/giampaolo/psutil
Source0:        https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires:  gcc
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-devel
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-rpm-macros
# Test dependencies
%if %{with tests}
BuildRequires:  procps-ng
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-mock
%endif

%description
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.

%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%autosetup -p0 -n %{srcname}-release-%{version}

# Remove shebangs
find psutil -name \*.py | while read file; do
  sed -i.orig -e '1{/^#!/d}' $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done

%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%py3_build

%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%py3_install

%{?scl:EOF}


%if %{with tests}
%check
%{?scl:scl enable %{scl} - << \EOF}
set -ex
make test-memleaks PYTHON=%{__python3}

%{?scl:EOF}
%endif

%files
%license LICENSE
%doc CREDITS HISTORY.rst README.rst
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/*.egg-info


%changelog
* Tue Feb 04 2020 Lumír Balhar <lbalhar@redhat.com> - 5.6.4-4
- Import from the python38 module and modified for rh-python38 RHSCL
Resolves: rhbz#1671025

* Thu Dec 12 2019 Tomas Orsava <torsava@redhat.com> - 5.6.4-3
- Exclude unsupported i686 arch

* Wed Nov 20 2019 Lumír Balhar <lbalhar@redhat.com> - 5.6.4-2
- Adjusted for Python 3.8 module in RHEL 8

* Wed Nov 06 2019 Lumír Balhar <lbalhar@redhat.com> - 5.6.4-1
- New upstream release 5.6.4
- bcond for Python 2 subpackage and tests
- Enabled tests

* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 5.6.3-5
- Add python2-setuptools to BuildRequires to fix egg info. Fixes bug #1750362

* Tue Sep 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.6.3-4
- Reduce unused build dependencies

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 5.6.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Kevin Fenzi <kevin@scrye.com> - 5.6.3-1
- Update to 5.6.3 Fixes bug #1567102

* Thu Feb 28 2019 Yatin Karel <ykarel@redhat.com> - 5.5.1-1
- Update to 5.5.1 (Resolves #1567102)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 5.4.3-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.4.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Jan 22 2018 Gwyn Ciesla <limburgher@gmail.com> - 5.4.3-2
- Disable tests entirely.

* Mon Jan 22 2018 Gwyn Ciesla <limburgher@gmail.com> - 5.4.3-1
- 5.4.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 23 2017 Kevin Fenzi <kevin@scrye.com> - 5.2.2-1
- Update to 5.2.2. Fixes bug #1441010

* Sat Mar 25 2017 Kevin Fenzi <kevin@scrye.com> - 5.2.1-1
- Update to 5.2.1. Fixes bug #1418489

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 5.1.3-1
- Update to 5.1.3. Fixes bug #1418489

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Kevin Fenzi <kevin@scrye.com> - 5.0.1-1
- Update to 5.0.1. Fixes bug #1389579
- Disable failing test while upstream looks at it. 

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 5.0.0-1
- Update to 5.0.0. Fixes bug #1389579

* Tue Oct 25 2016 Kevin Fenzi <kevin@scrye.com> - 4.4.0-1
- Update to 4.4.0. Fixes bug #1387942

* Sat Sep 03 2016 Kevin Fenzi <kevin@scrye.com> - 4.3.1-1
- Update to 4.3.1. Fixes bug #1372500

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 21 2016 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-1
- Update to 4.3.0

* Mon May 16 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-6
- Use modern provides filter
- Update URL
- Use %%python3_pkgversion for EPEL7 compat

* Fri Mar 11 2016 Than Ngo <than@redhat.com> - 3.2.1-5
- fix endian issue on s390x/ppc64

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep  4 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.2.1-2
- Add Obsoletes for old package

* Fri Sep  4 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1
- Update to latest Python guidelines (https://fedorahosted.org/fpc/ticket/281)

* Wed Jul 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.1.1-2
- Restore *.so files
- Enable tests

* Tue Jul 21 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 2.2.0-1
- new version

* Wed Dec  3 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 1.2.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Jan 06 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Fri Aug 16 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 19 2012 Mohamed El Morabity <melmorabity@fedorapeople.org> - 0.6.1-1
- Update to 0.6.1

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.1-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Sun Nov 20 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Mon Jul 18 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Wed Mar 23 2011 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1
- Spec cleanup

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.3-5
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Fri Jul 30 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.3-4
- bump, because previous build nvr already existed in F-14

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.3-2
- Add missing popd in %%build

* Sat Mar 27 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.3-1
- Update to 0.1.3
- Remove useless call to 2to3 and corresponding BuildRequires
  python2-tools (this version supports Python 3)

* Sat Feb 20 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-4
- Change python-utils BuildRequires for python2-utils

* Sat Feb 20 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-3
- Add python3 subpackage

* Thu Jan 14 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-2
- Drop no-shebang patch for a sed command
- Drop test suite from %%doc tag

* Fri Jan  8 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-1
- Initial RPM release