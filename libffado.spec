%define lib_major       2
%define lib_name        %mklibname ffado %{lib_major}
%define lib_name_devel  %mklibname ffado -d

Name:           libffado
Summary:        Firewire audio drivers for JACK
Version:        2.1.0
Release:        1

Source:         http://www.ffado.org/files/%{name}-%{version}.tgz
URL:            http://www.ffado.org/
License:        GPLv2+ and GPLv3
Group:          Sound

BuildRequires:  scons, pkgconfig
BuildRequires:  libraw1394-devel, libiec61883-devel, libavc1394-devel
BuildRequires:  libxml++-devel
BuildRequires:  python-qt4-devel, expat-devel, dbus-devel
BuildRequires:  python-dbus dbus-c++-devel python-qt4-dbus

%description
The FFADO library provides a generic, open-source solution for the
support of FireWire based audio devices for the Linux platform. It is the
successor of the FreeBoB project. Currently this library is used by the
firewire backends of the jack audio connection kit sound server
(jackit package). This backend provides audio and midi support,
and is available in both jack1 and jack2.

#-----------------------------------
%package -n %{lib_name}

Summary:        Firewire audio drivers for JACK
Group:          Sound

%description -n %{lib_name}
The FFADO library provides a generic, open-source solution for the
support of FireWire based audio devices for the Linux platform. It is the
successor of the FreeBoB project. Currently this library is used by the
firewire backends of the jack audio connection kit sound server
(jackit package). This backend provides audio and midi support,
and is available in both jack1 and jack2.

%files -n %{lib_name}
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE.* README
%{_libdir}/libffado.so.*
/lib/udev/rules.d/60-ffado.rules

#-----------------------------------
%package -n ffado
Summary:        Firewire audio driver applications and utilities
Group:          Sound
Requires:       %{lib_name} = %{version}-%{release}
Requires:       python-dbus, qt4-qtdbus
Requires:       python-qt4

%description -n ffado
Configuration utilities for the FFADO firewire drivers

%files -n ffado
%defattr(-,root,root,-)
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

#-----------------------------------
%package -n %{lib_name_devel}
Summary:        Firewire audio driver library development headers
Group:          Sound
Requires:       %{lib_name} = %{version}-%{release}
Requires:       pkgconfig, libxml++-devel
Requires:       libiec61883-devel, libavc1394-devel, libraw1394-devel
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{lib_name_devel}
Development files needed to build applications against libffado.

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------
%prep
%setup -q -n %{name}-%{version}

%build
scons PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir}

%install
scons PREFIX=%{_prefix} LIBDIR=%{_libdir} \
      DESTDIR=%{buildroot} install

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


%changelog
* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-4mdv2011.0
+ Revision: 660246
- mass rebuild

* Sun Oct 17 2010 Frank Kober <emuse@mandriva.org> 2.0.1-3mdv2011.0
+ Revision: 586202
- kill qt3 dependency for devel package as well

* Sun Oct 10 2010 Frank Kober <emuse@mandriva.org> 2.0.1-2mdv2011.0
+ Revision: 584640
- remove obsolete dbus-qt3 BR

* Thu Jul 15 2010 Frank Kober <emuse@mandriva.org> 2.0.1-1mdv2011.0
+ Revision: 553651
- new version 2.0.1 now working with new fw kernel stack

* Sat Mar 20 2010 Frank Kober <emuse@mandriva.org> 2.0.0-3mdv2010.1
+ Revision: 525563
- add python-qt4 to Requires, bump release

* Sun Feb 28 2010 Frank Kober <emuse@mandriva.org> 2.0.0-2mdv2010.1
+ Revision: 512749
- rebuild with dependencies in main/release

* Sat Feb 27 2010 Frank Kober <emuse@mandriva.org> 2.0.0-1mdv2010.1
+ Revision: 512339
-update group tag
-add python-dbus BR
-fix icon path
- import ffado version 2.0.0
- import libffado


