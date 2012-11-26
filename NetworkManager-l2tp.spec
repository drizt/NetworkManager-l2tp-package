%global nm_version          1:0.9.2
%global dbus_version        1.1
%global gtk3_version        3.0
%global ppp_version         2.4.5
%global shared_mime_version 0.16-3

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.9.6
Release:   2%{?dist}
License:   GPLv2+ and LGPLv2+
Group:     System Environment/Base
URL:       https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source:    https://github.com/seriyps/NetworkManager-l2tp/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: gtk3-devel             >= %{gtk3_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.74
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: libgnome-keyring-devel
BuildRequires: intltool gettext
BuildRequires: ppp-devel = %{ppp_version}

Requires: nm-connection-editor
Requires: dbus             >= %{dbus_version}
Requires: NetworkManager   >= %{nm_version}
Requires: ppp              = %{ppp_version}
Requires: shared-mime-info >= %{shared_mime_version}
Requires: pptp
Requires: gnome-keyring
Requires: xl2tpd

%filter_provides_in %{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
%filter_provides_in %{_libdir}/NetworkManager/lib*.so

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q


%build
./autogen.sh
%configure \
    --disable-static \
    --enable-more-warnings=yes \
    --with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}

make %{?_smp_mflags}

%install

make install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

rm -f %{buildroot}%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.la
rm -f %{buildroot}%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.a

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
# Content must not be changed
%config %{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libdir}/NetworkManager/lib*.so
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
%{_libexecdir}/nm-l2tp-auth-dialog
%{_libexecdir}/nm-l2tp-service
%{_datadir}/gnome-vpn-properties/l2tp

%changelog
* Mon Nov 26 2012  <drizt@land.ru> - 0.9.6-2
- corrected License tag. Added LGPLv2+
- use only %%{buildroot}
- use %%config for configuration files
- removed unused scriptlets
- cleaned .spec file
- preserve timestamps when installing
- filtered provides for plugins
- droped zero-length changelog
- use %%global instead of %%define

* Mon Nov 19 2012  <drizt@land.ru> - 0.9.6-1
- initial version based on NetworkManager-pptp 1:0.9.3.997-3

