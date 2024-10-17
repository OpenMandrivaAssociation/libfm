%define api 1.0
%define major 4
%define libname	%mklibname fm
%define elibname	%mklibname fm-extra
%define glibname	%mklibname fm-gtk3
%define devname	%mklibname -d fm
%define edevname	%mklibname -d fm-extra

%define oldlibname	%mklibname fm 4
%define oldelibname	%mklibname fm-extra 4
%define oldglibname	%mklibname fm-gtk 3 4

# git snapshot
%global snapshot 1
%if 0%{?snapshot}
	%global commit		5346a5390a0881d5713a71e15f371132680056ee
	%global commitdate	20230916
	%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

%bcond_without gtk

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	1.3.2
Release:	2
Source0:	https://github.com/lxde/libfm/archive/%{?snapshot:%{commit}}%{!?snapshot:%{version}}/%{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}.tar.gz
License:	GPLv2
Group:		File tools
Url:		https://pcmanfm.sourceforge.net/
Patch0:		libfm-0.1.5-set-cutomization.patch
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(cairo) >= 1.8.0
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.26.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libmenu-cache) >= 0.3.2
BuildRequires:	pkgconfig(pango) >= 1.16.0
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
%if %{without gtk}
Obsoletes:	lxshortcut <= 1.2.3-2
%endif
BuildRequires:	vala

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/terminals.list
%{_datadir}/%{name}/archivers.list
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/libfm

#---------------------------------------------------------------------------

%package gtk
Summary:	gtk related parts of the %{name} library
Group:		File tools
Requires:	lxshortcut = %{EVRD}
Obsoletes:	%oldlibname < %{EVRD}

%description gtk
gtk related parts of the %{name} library

%files gtk
%if %{with gtk}
%{_bindir}/libfm-pref-apps
%{_mandir}/man1/libfm-pref-apps.1*
%{_datadir}/applications/libfm-pref-apps.desktop
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/*
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	%{name} library package
Group:		File tools
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
%{summary}.

%files -n %{libname}
%{_libdir}/libfm.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{elibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}
Obsoletes:	%oldelibname < %{EVRD}

%description -n %{elibname}
%{summary}

%files -n %{elibname}
%{_libdir}/libfm-extra.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{glibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}
Obsoletes:	%oldglibname < %{EVRD}

%description -n %{glibname}
%{summary}

%files -n %{glibname}
%if %{with gtk}
%{_libdir}/libfm-gtk3.so.%{major}*
%endif
#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	%{name} developement files
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
%if %{with gtk}
Requires:	%{glibname} = %{version}-%{release}
%endif
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files needed when building applications based on
%{name}.

%files -n %{devname}
#doc #{_datadir}/gtk-doc/html/*
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}-%{api}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}-%{api}/*.h
%exclude %{_includedir}/%{name}/fm-xml-file.h
%exclude %{_includedir}/%{name}/fm-version.h
%exclude %{_includedir}/%{name}/fm-extra.h
%exclude %{_includedir}/%{name}-%{api}/fm-xml-file.h
%exclude %{_includedir}/%{name}-%{api}/fm-version.h
%exclude %{_includedir}/%{name}-%{api}/fm-extra.h
%{_libdir}/libfm.so
%{_libdir}/pkgconfig/libfm.pc
%if %{with gtk}
%{_libdir}/libfm-gtk3.so
%{_libdir}/pkgconfig/libfm-gtk3.pc
%endif
%endif

#---------------------------------------------------------------------------

%package -n %{edevname}
Summary:	%{name}-extra developement files
Group:		File tools
Requires:	%{elibname} = %{version}-%{release}

%description -n %{edevname}
This package contains header files needed when building applications based on
%{name}-extra.

%files -n %{edevname}
%{_libdir}/libfm-extra.so
%{_libdir}/pkgconfig/libfm-extra.pc
%{_includedir}/%{name}/fm-xml-file.h
%{_includedir}/%{name}/fm-version.h
%{_includedir}/%{name}/fm-extra.h
%{_includedir}/%{name}-%{api}/fm-xml-file.h
%{_includedir}/%{name}-%{api}/fm-version.h
%{_includedir}/%{name}-%{api}/fm-extra.h

#---------------------------------------------------------------------------

%package -n lxshortcut
Summary:	Edit app shortcuts
Group:		Graphical desktop/Other

%description -n lxshortcut
LXShortcut is a small program used to edit application shortcuts created
with freedesktop.org Desktop Entry spec.

%files -n lxshortcut
%if %{with gtk}
%{_bindir}/lxshortcut
%{_datadir}/applications/lxshortcut.desktop
%{_mandir}/man1/lxshortcut.1*
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}

%build
autoreconf -fiv
%configure \
	--enable-udisks \
	--with%{?with_gtk:-gtk=3}%{?!with_gtk:out-gtk} \
	%{nil}
%make_build

%install
%make_install

#some hack for avoid upgrade error
#copy all in libfm-1.0 in includedir to libfm instead symlink, rather early it is true
rm -rf %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -f %{buildroot}%{_includedir}/%{name}-%{api}/* %{buildroot}%{_includedir}/%{name}/

# locales
%find_lang %{name}


