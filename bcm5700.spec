#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart sieciowych Broadcom NetXtreme BCM57xx
Name:		bcm5700
Version:	8.3.14
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
# extracted from http://www.broadcom.com/docs/driver_download/570x/linux-8.3.14.zip
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	6dd814821f26ad67c7d7ce61c5275ca0
Source1:	%{name}-Makefile
Patch0:		%{name}-2.6.22.patch
URL:		http://www.broadcom.com/drivers/downloaddrivers.php
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Broadcom's NetXtreme
BCM57xx Network Interface Cards.

%description -l pl.UTF-8
Pakiet zawiera sterownik dla Linuksa do kart sieciowych Broadcom
BCM57xx.

%package -n kernel-net-bcm5700
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel-net-bcm5700
Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface
Cards.

%description -n kernel-net-bcm5700 -l pl.UTF-8
Sterownik dla Linuksa do kart sieciowych Broadcom BCM57xx.

%prep
%setup -q
%patch0 -p1

%build
%build_kernel_modules -C src -m bcm5700

%install
rm -rf $RPM_BUILD_ROOT
cd src

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install bcm5700.4 $RPM_BUILD_ROOT%{_mandir}/man4
%endif

%if %{with kernel}
%install_kernel_modules -m bcm5700 -d kernel/drivers/net
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-bcm5700
%depmod %{_kernel_ver}

%postun	-n kernel-net-bcm5700
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README.TXT
%{_mandir}/man4/bcm5700.*
%endif

%if %{with kernel}
%files -n kernel-net-bcm5700
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/bcm5700.ko*
%endif
