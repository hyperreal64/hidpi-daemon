%global srcname hidpi-daemon
%define hidpidir %{buildroot}/%{name}-%{version}

Name:           hidpi-daemon
Version:        33
Release:        1%{?dist}
Summary:        System76 HiDPI Daemon to manage HiDPI and LoDPI monitors on X
License:        GPLv2+
URL:            https://github.com/pop-os/hidpi-daemon
Source0:        https://github.com/hyperreal64/hidpi-daemon/archive/%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel,python3-setuptools,python3-pyflakes
Requires:       python3-xlib,python3-pydbus,acpid

%description
System76 HiDPI Daemon to manage HiDPI and LoDPI monitors on X.

This package contains a Fedora-adapted version of the upstream source.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

# extract SOURCE0 archive into buildroot
tar xf %{SOURCE0} -C %{buildroot}

# create _bindir under buildroot
mkdir -p %{buildroot}/%{_bindir}

# create _datarootdir with subdirectories applications and glib-2.0/schemas
mkdir -p %{buildroot}/%{_datarootdir}/{applications,glib-2.0/schemas}

# copy files from extracted SOURCE0 to appropriate directories under buildroot
cp %{hidpidir}/hidpi-daemon %{buildroot}/%{_bindir}
cp %{hidpidir}/hidpi-notification %{buildroot}/%{_bindir}
cp %{hidpidir}/hidpi-daemon.desktop %{buildroot}/%{_datarootdir}/applications
cp %{hidpidir}/hidpi-frontend.desktop %{buildroot}/%{_datarootdir}/applications
cp %{hidpidir}/com.system76.hidpi.gschema.xml %{buildroot}/%{_datarootdir}/glib-2.0/schemas

# remove hidpidir
rm -rf %{hidpidir}

%check
%{python3} setup.py test

%clean
rm -rf %{buildroot}

%files
%{_bindir}/hidpi-daemon
%{_bindir}/hidpi-notification
%{_datarootdir}/applications/hidpi-daemon.desktop
%{_datarootdir}/applications/hidpi-frontend.desktop
%{_datarootdir}/glib-2.0/schemas
%license LICENSE
%doc README.md
%{python3_sitelib}/hidpidaemon-*.egg-info
%{python3_sitelib}/hidpidaemon/

# compile glib schemas
%post
glib-compile-schemas %{_datarootdir}/glib-2.0/schemas

%changelog
* Tue Jan 26 2021 Jeffrey Serio <hyperreal64@pm.me>
- Initial version of package for Fedora 33
