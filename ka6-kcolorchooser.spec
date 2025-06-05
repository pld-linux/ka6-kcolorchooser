#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kcolorchooser
Summary:	KColorChooser
Name:		ka6-%{kaname}
Version:	25.04.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	cc07eda2a23ba443cc3c0687ec1e34ad
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KColorChooser is a simple application to select the color from the
screen or from a pallete.

Features:

Select colors from any location on the screen. Select colors from a
range of standard palletes available. Color values shown in
Hue-Saturation-Value (HSV), Red-Green-Blue (RGB) and HTML formats.

%description -l pl.UTF-8
KColorChooser jest prostą aplikacją do wybrania koloru z ekranu
lub z palety.

Właściwości:

Zaznaczenie kolorów z dowolnej lokalizacji na ekranie. Wybieranie
kolorów z zestawu standardowych palet. Wartości są pokazywane
W Hue-Saturation-Value (HSV), Red-Green-Blue (RGB) i w formacie
HTML.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kcolorchooser
%{_desktopdir}/org.kde.kcolorchooser.desktop
%{_iconsdir}/hicolor/16x16/apps/kcolorchooser.png
%{_iconsdir}/hicolor/22x22/apps/kcolorchooser.png
%{_datadir}/metainfo/org.kde.kcolorchooser.appdata.xml
