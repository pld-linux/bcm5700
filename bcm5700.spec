#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%ifarch sparc
%undefine	with_smp
%endif

Summary:	Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych Broadcom NetXtreme BCM57xx
Name:		bcm5700
Version:	8.2.18
%define		_rel	5
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
# extracted from http://www.broadcom.com/docs/driver_download/570x/linux-8.1.55.zip
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	44985b0aebf031c343d4f29b5432cf85
Source1:	%{name}-Makefile
URL:		http://www.broadcom.com/drivers/downloaddrivers.php
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards.

%description -l pl
Pakiet zawiera sterownik dla Linuksa do kart sieciowych Broadcom BCM57xx.

%package -n kernel-net-bcm5700
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-net-bcm5700
Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards.

%description -n kernel-net-bcm5700 -l pl
Sterownik dla Linuksa do kart sieciowych Broadcom BCM57xx.

%package -n kernel-smp-net-bcm5700
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-net-bcm5700
Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards.

%description -n kernel-smp-net-bcm5700 -l pl
Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx.

%prep
%setup -q

%build
cd src

%if %{with kernel}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts

	install %{SOURCE1} Makefile

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		%{?debug:DBG=1} \
%if "%{_target_base_arch}" != "%{_arch}"
                ARCH=%{_target_base_arch} \
                CROSS_COMPILE=%{_target_base_cpu}-pld-linux- \
%endif
                HOSTCC="%{__cc}" \
		CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv bcm5700{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd src

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install bcm5700.4 $RPM_BUILD_ROOT%{_mandir}/man4
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net
install bcm5700-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/bcm5700.ko
%if %{with smp} && %{with dist_kernel}
install bcm5700-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/bcm5700.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-bcm5700
%depmod %{_kernel_ver}

%postun	-n kernel-net-bcm5700
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-bcm5700
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-bcm5700
%depmod %{_kernel_ver}smp

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

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-bcm5700
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/bcm5700.ko*
%endif
%endif
