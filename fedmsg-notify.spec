Summary:	Fedmsg Desktop Notifications
Name:		fedmsg-notify
Version:	0.5.5
Release:	0.2
License:	GPL v3+
Group:		X11/Applications/Networking
Source0:	https://github.com/fedora-infra/fedmsg-notify/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fc6fe17a2c385c99e0165df5b0a7560e
Patch0:		pld.patch
URL:		https://github.com/fedora-infra/fedmsg-notify
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	python-pygobject3
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
Requires:	fedmsg >= 0.5.5
Requires:	glib2 >= 1:2.26.0
#Requires:	python-fedmsg-meta-fedora-infrastructure
#Requires:	python-fedora
Requires:	python-psutil
Requires:	python-pygobject3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	busname org.fedoraproject.fedmsg.notify

%description
fedmsg-notify provides a dbus-activated daemon that subscribes to
realtime messages from Fedora Infrastructure and displays them as
desktop notifications. It also comes with a fedmsg-notify-config tool
to enable/disable the service.

%prep
%setup -q
%patch0 -p1

# install pld
touch fedmsg_notify/distro_specific/_pld.py
# skip fedora and debian
mv fedmsg_notify/distro_specific/_debian.py .
mv fedmsg_notify/distro_specific/_fedora.py .

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

# DBus configuration
install -d $RPM_BUILD_ROOT{%{_datadir}/dbus-1/services,%{_sysconfdir}/dbus-1/system.d}
cp -p conf/%{busname}.service $RPM_BUILD_ROOT%{_datadir}/dbus-1/services/%{busname}.service
cp -p conf/%{busname}.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/%{busname}.conf

# fedmsg-notify-config desktop file
desktop-file-install \
    --dir=$RPM_BUILD_ROOT%{_desktopdir} \
    conf/%{name}-config.desktop

# fedmsg-notify-deaemon desktop file
desktop-file-install \
    --dir=$RPM_BUILD_ROOT%{_desktopdir} \
    conf/%{name}-daemon.desktop

# Autostart the daemon
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
cp -p $RPM_BUILD_ROOT%{_desktopdir}/%{name}-daemon.desktop \
    $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/

# GSettings schema
install -d $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas
cp -p conf/%{busname}.gschema.xml $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ $1 -eq 0 ]; then
	%glib_compile_schemas
fi

%posttrans
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
/etc/xdg/autostart/%{name}-daemon.desktop
/etc/dbus-1/system.d/%{busname}.conf
%attr(755,root,root) %{_bindir}/%{name}-daemon
%attr(755,root,root) %{_bindir}/%{name}-config
%{_datadir}/dbus-1/services/%{busname}.service
%{_datadir}/glib-2.0/schemas/%{busname}.gschema.xml
%{_desktopdir}/%{name}-config.desktop
%{_desktopdir}/%{name}-daemon.desktop

%dir %{py_sitescriptdir}/fedmsg_notify
%{py_sitescriptdir}/fedmsg_notify/*.py[co]
%dir %{py_sitescriptdir}/fedmsg_notify/distro_specific
%{py_sitescriptdir}/fedmsg_notify/distro_specific/__init__.py[co]
%{py_sitescriptdir}/fedmsg_notify/distro_specific/_pld.py[co]
%{py_sitescriptdir}/fedmsg_notify-%{version}-py*.egg-info
