%if 0%{?fedora}
%global with_python3 1
%endif

%define name certmonger-comodo-helper
%define version 0.2.2
%define unmangled_version 0.2.2
%define release 2
# The description
%define desc The certmonger_comodo_helper is a helper for certmonger that submits and gathers certificates from the Comodo API. It is written in python and requires the suds python library, it should be compatible with both python 3 and 2.
# The summary
%define sum A certmonger helper to access the comodo API.
# The requirements
%define req certmonger
# The name for the package is slightly different than the module name.
%define pkg_name certmonger_comodo_helper

Summary: %{sum}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: https://github.com/erinn/certmonger_comodo_helper/archive/v%{unmangled_version}.tar.gz#/%{pkg_name}-%{unmangled_version}.tar.gz
License: AGPL-3.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Requires: %req
BuildArch: noarch
Url: https://github.com/erinn/certmonger_comodo_helper

%description
%{desc}

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        %{sum}
BuildRequires: python3-devel
BuildRequires: python3-suds
BuildRequires: python3-setuptools

%description -n python3-%{name}
%{desc}

%else

%package -n python2-%{name}
Summary:        %{sum}
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-suds
%{?python_provide:%python_provide python2-%{name}}
Requires: certmonger python-suds

%description -n python2-%{name}
%{desc}
%endif

%prep
%setup -n %{pkg_name}-%{unmangled_version} -n %{pkg_name}-%{unmangled_version}
%if 0%{?with_python3}
sed -i 's/suds/suds-jurko/' setup.py
%endif

%build
%if 0%{?with_python3}
%py3_build
%else
%py2_build
%endif

%install
%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-scripts usr/libexec/certmonger
mkdir -p $RPM_BUILD_ROOT/etc/certmonger/
mkdir -p $RPM_BUILD_ROOT/var/lib/certmonger/cas/
mkdir -p $RPM_BUILD_ROOT/usr/libexec/certmonger/
install -m 640 etc/comodo.ini $RPM_BUILD_ROOT/etc/certmonger/
install -m 640 etc/comodo $RPM_BUILD_ROOT/var/lib/certmonger/cas/
%else
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-scripts usr/libexec/certmonger
mkdir -p $RPM_BUILD_ROOT/etc/certmonger/
mkdir -p $RPM_BUILD_ROOT/var/lib/certmonger/cas/
mkdir -p $RPM_BUILD_ROOT/usr/libexec/certmonger/
install -m 640 etc/comodo.ini $RPM_BUILD_ROOT/etc/certmonger/
install -m 640 etc/comodo $RPM_BUILD_ROOT/var/lib/certmonger/cas/
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
%else
%{__python2} setup.py test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
%files -n python3-%{name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/*
%{_libexecdir}/certmonger/certmonger_comodo_helper
%config(noreplace) /var/lib/certmonger/cas/comodo
%config(noreplace) /etc/certmonger/comodo.ini
%else
%files -n python2-%{name}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/*
%{_libexecdir}/certmonger/certmonger_comodo_helper
%config(noreplace) /var/lib/certmonger/cas/comodo
%config(noreplace) /etc/certmonger/comodo.ini
%endif


%changelog
* Tue Sep 26 2017 looneytr - 0.2.2-2
- Make /var/lib/certmonger/cas/comodo a config file again with noreplace

* Fri Sep 22 2017 looneytr - 0.2.2-1
- New release.

* Fri Sep 22 2017 looneytr - 0.2.1-1
- Update spec to use proper version tags

* Fri Sep 22 2017 looneytr - 0.2.0-2
- Modify config to noreplace

* Wed Sep 20 2017 looneytr - 0.2.0-1
- New release.

* Wed Sep 20 2017 looneytr - 0.1.0-5
- Fix config files.

* Wed Sep 20 2017 looneytr - 0.1.0-4
- Add dependency on certmonger.

* Wed Sep 20 2017 looneytr - 0.1.0-3
- Fix summary.

* Wed Sep 20 2017 looneytr - 0.1.0-2
- Initial release.