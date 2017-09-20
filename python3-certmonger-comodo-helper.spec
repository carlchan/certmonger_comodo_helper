%define name certmonger-comodo-helper
%define version 0.1.0
%define unmangled_version 0.1.0
%define release 1
%define desc The certmonger_comodo_helper is a helper for certmonger that submits and gathers certificates from the Comodo API. It is written in python and requires the suds python library, it should be compatible with both python 3 and 2.
%define sum A certmonger helper to access the comodo API.

# The name for the package is slightly different than the module name.
%define pkg_name certmonger_comodo_helper

Summary: %{sum}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{pkg_name}-%{unmangled_version}.tar.gz
License: AGPL-3.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Requires: certmonger
BuildArch: noarch
BuildRequires: python3-devel python3-setuptools python3-suds certmonger
Url: https://github.com/erinn/certmonger_comodo_helper

%description
%{desc}

%package -n python3-%{name}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
%{desc}

%prep
%setup -n %{pkg_name}-%{unmangled_version} -n %{pkg_name}-%{unmangled_version}

%build
%py3_build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-scripts usr/libexec/certmonger
mkdir -p $RPM_BUILD_ROOT/etc/certmonger/
mkdir -p $RPM_BUILD_ROOT/var/lib/certmonger/cas/
mkdir -p $RPM_BUILD_ROOT/usr/libexec/certmonger/
install -m 640 etc/comodo.ini $RPM_BUILD_ROOT/etc/certmonger/
install -m 640 etc/comodo $RPM_BUILD_ROOT/var/lib/certmonger/cas/

%check
%{__python3} setup.py test

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/*
%config /etc/certmonger/comodo.ini
%config /var/lib/certmonger/cas/comodo
%{_libexecdir}/certmonger/certmonger_comodo_helper
