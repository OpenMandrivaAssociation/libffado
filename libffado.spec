%define name    libffado
%define version 2.0.0
%define release %mkrel 1

%define lib_major       2
%define lib_name        %mklibname ffado %{lib_major} 
%define lib_name_devel  %mklibname ffado -d

Name:           %{name} 
Summary:        Firewire audio drivers for JACK
Version:        %{version} 
Release:        %{release}

Source:         http://www.ffado.org/files/%{name}-%{version}.tar.gz
URL:            http://www.ffado.org/
License:        GPLv2+ and GPLv3
Group:          Sound

BuildRequires:  scons, pkgconfig
BuildRequires:  libraw1394-devel, libiec61883-devel, libavc1394-devel
BuildRequires:  libxml++-devel
BuildRequires:  python-qt4-devel, expat-devel, dbus-devel
BuildRequires:  libdbus-qt-1-devel
BuildRequires:  python-dbus

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

#-----------------------------------
%package -n ffado
Summary:        Firewire audio driver applications and utilities
Group:          Sound
Requires:       %{lib_name} = %{version}-%{release}
Requires:       python-dbus, qt4-qtdbus

%description -n ffado
Configuration utilities for the FFADO firewire drivers

%files -n ffado
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/python
%{_datadir}/%{name}/configuration
%{_datadir}/applications/mandriva-ffado-mixer.desktop
%{_datadir}/%{name}/icons/hi64-apps-ffado.png

#-----------------------------------
%package -n %{lib_name_devel}
Summary:        Firewire audio driver library development headers
Group:          Development/Libraries
Requires:       %{lib_name} = %{version}-%{release}
Requires:       pkgconfig, libxml++-devel
Requires:       libdbus-qt-1-devel
Requires:       libraw1394-devel, libiec61883-devel, libavc1394-devel
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
scons PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
rm -rf %{buildroot}

scons PREFIX=%{_prefix} LIBDIR=%{_libdir} \
      DESTDIR=%{buildroot} install

install -m 0644 support/tools/listirqinfo.py %{buildroot}%{_datadir}/libffado/python
install -m 0644 support/tools/helpstrings.py %{buildroot}%{_datadir}/libffado/python

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif


%changelog
