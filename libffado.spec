%define lib_major 2
%define lib_name %mklibname ffado %{lib_major}
%define lib_name_devel %mklibname ffado -d

Name:		libffado
Summary:	Firewire audio drivers for JACK
Version:	2.4.7
Release:	1
Source0:	http://www.ffado.org/files/%{name}-%{version}.tgz
URL:		http://www.ffado.org/
License:	GPLv2+ and GPLv3
Group:		Sound

BuildRequires:	scons
BuildRequires:	pkgconfig
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:	pkgconfig(libraw1394)
BuildRequires:	pkgconfig(libiec61883)
BuildRequires:	pkgconfig(libavc1394)
BuildRequires:	pkgconfig(libxml++-2.6)
BuildRequires:	python3dist(pyqt5)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	python-dbus
#BuildRequires:	pkgconfig(dbus-c++-1)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	python-qt5-dbus

%description
The FFADO library provides a generic, open-source solution for the
support of FireWire based audio devices for the Linux platform. It is the
successor of the FreeBoB project. Currently this library is used by the
firewire backends of the jack audio connection kit sound server
(jackit package). This backend provides audio and midi support,
and is available in both jack1 and jack2.


%package -n %{lib_name}
Summary:	Firewire audio drivers for JACK
Group:		Sound

%description -n %{lib_name}
The FFADO library provides a generic, open-source solution for the
support of FireWire based audio devices for the Linux platform. It is the
successor of the FreeBoB project. Currently this library is used by the
firewire backends of the jack audio connection kit sound server
(jackit package). This backend provides audio and midi support,
and is available in both jack1 and jack2.

%files -n %{lib_name}
%{_libdir}/libffado.so.%{lib_major}*
/lib/udev/rules.d/60-ffado.rules


%package -n ffado
Summary:		Firewire audio driver applications and utilities
Group:			Sound
Requires:		%{lib_name} = %{version}-%{release}
Requires:		python-dbus
Requires:		qt4-qtdbus
Requires:		python-qt4
Conflicts:		%{mklibname ffado 2} < 2.1.0-2

%description -n ffado
Configuration utilities for the FFADO firewire drivers.

%files -n ffado
%doc AUTHORS ChangeLog LICENSE.* README
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/python
%{_datadir}/%{name}/configuration
%{_datadir}/%{name}/*.xml
%{_datadir}/applications/mandriva-ffado-mixer.desktop
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/hi64-apps-ffado.png
%{python_sitelib}/ffado/*.ui
%{python_sitelib}/ffado/*.py
%{python_sitelib}/ffado/mixer/*.ui
%{python_sitelib}/ffado/mixer/*.py
%{python_sitelib}/ffado/widgets/*.py
%{_datadir}/dbus-1/services/org.ffado.Control.service
%doc %{_mandir}/man1/*

%package -n %{lib_name_devel}
Summary:		Firewire audio driver library development headers
Group:			Sound
Requires:		%{lib_name} = %{version}-%{release}
Requires:		pkgconfig
Requires:		libxml++-devel
Requires:		libiec61883-devel
Requires:		libavc1394-devel
Requires:		libraw1394-devel
Provides:		%{name}-devel = %{version}-%{release}

%description -n %{lib_name_devel}
Development files needed to build applications against libffado.

%files -n %{lib_name_devel}
%{_libdir}/%{name}.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{name}.pc

%prep
%setup -q

%build
%scons PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir}

%install
%scons_install PREFIX=%{_prefix} LIBDIR=%{_libdir}

install -m 0755 support/tools/listirqinfo.py %{buildroot}%{_datadir}/libffado/python
install -m 0755 support/tools/helpstrings.py %{buildroot}%{_datadir}/libffado/python
chmod a+x %{buildroot}%{_datadir}/libffado/python/*.py

sed -i -e '1i#!/usr/bin/python' %{buildroot}%{_datadir}/libffado/python/ffado_diag_helpers.py
sed -i -e '1i#!/usr/bin/python' %{buildroot}%{_datadir}/libffado/python/helpstrings.py

rm -rf %{buildroot}%{_bindir}/test-dice-eap

mkdir -p %{buildroot}%{_datadir}/applications
#make desktop file
cat > %{buildroot}%{_datadir}/applications/mandriva-ffado-mixer.desktop <<EOF
[Desktop Entry]
Name=Ffado Mixer
Comment=Mixer for Firewire Audio Devices
Exec=%{_bindir}/ffado-mixer
Icon=%{_datadir}/%{name}/icons/hi64-apps-ffado.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;
EOF
