#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%ifarch sparc
%undefine	with_smp
%endif

%define		pname	bcm5700
Summary:	Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart sieciowych Broadcom NetXtreme BCM57xx
Name:		%{pname}%{_alt_kernel}
Version:	8.3.14
Release:	3
License:	GPL v2
Group:		Base/Kernel
# extracted from http://www.broadcom.com/docs/driver_download/570x/linux-8.3.14.zip
Source0:	%{pname}-%{version}.tar.gz
# Source0-md5:	6dd814821f26ad67c7d7ce61c5275ca0
Source1:	%{pname}-Makefile
URL:		http://www.broadcom.com/drivers/downloaddrivers.php
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Broadcom's NetXtreme
BCM57xx Network Interface Cards.

Note: this driver is obsoleted by Broadcom, use tg3 instead.

%description -l pl.UTF-8
Pakiet zawiera sterownik dla Linuksa do kart sieciowych Broadcom
BCM57xx.

Uwaga: ten sterownik Broadcomu jest przestarzały, należy używać tg3.

%package -n kernel%{_alt_kernel}-net-bcm5700
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Group:		Base/Kernel
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-net-bcm5700
Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface
Cards.

Note: this driver is obsoleted by Broadcom, use tg3 instead.

%description -n kernel%{_alt_kernel}-net-bcm5700 -l pl.UTF-8
Sterownik dla Linuksa do kart sieciowych Broadcom BCM57xx.

Uwaga: ten sterownik Broadcomu jest przestarzały, należy używać tg3.

%package -n kernel%{_alt_kernel}-smp-net-bcm5700
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Group:		Base/Kernel
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-smp-net-bcm5700
Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network
Interface Cards.

Note: this driver is obsoleted by Broadcom, use tg3 instead.

%description -n kernel%{_alt_kernel}-smp-net-bcm5700 -l pl.UTF-8
Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx.

Uwaga: ten sterownik Broadcomu jest przestarzały, należy używać tg3.

%prep
%setup -q -n %{pname}-%{version}

mv src/Makefile{,.orig}
cat > src/Makefile << EOF
obj-m += bcm5700.o
bcm5700-objs := b57um.o b57proc.o tigon3.o autoneg.o 5701rls.o tcp_seg.o b57diag.o
EXTRA_CFLAGS = -DDBG=0 -DT3_JUMBO_RCV_RCB_ENTRY_COUNT=256 -DNICE_SUPPORT -DPCIX_TARGET_WORKAROUND=1 -DINCLUDE_TBI_SUPPORT -DINCLUDE_5701_AX_FIX=1
EOF

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

%post	-n kernel%{_alt_kernel}-net-bcm5700
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-bcm5700
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-bcm5700
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-bcm5700
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README.TXT
%{_mandir}/man4/bcm5700.*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-bcm5700
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/bcm5700.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-bcm5700
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/bcm5700.ko*
%endif
%endif
