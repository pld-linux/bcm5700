
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		_orig_name	bcm5700
%define		_rel 4

Summary:	Linux driver for the 3Com Gigabit Server BCM5700 (3c996) Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych gigabit ethernet BCM5700 (3c996)
Name:		kernel-net-%{_orig_name}
Version:	2.0.28
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://support.3com.com/infodeli/tools/nic/linux/%{_orig_name}-%{version}.tar.gz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc}
Obsoletes:	kernel-smp-net-%{_orig_name}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux driver for the 3Com Gigabit Server BCM5700 (3c996) Network
Interface Cards.

%description -l pl
Sterownik dla Linuksa do kart sieciowych gigabit ethernet BCM5700
(3c996). Obs³uguje karty o symbolach 3c996B-T i 3c996-SX.

%package -n kernel-smp-net-%{_orig_name}
Summary:	Linux SMP driver for the 3Com Gigabit Server BCM5700 (3c996) Network Interface Cards
Summary(pl):	Sterownik dla Linuksa SMP do kart sieciowych gigabit ethernet BCM5700 (3c996)
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	kernel-net-%{_orig_name}

%description -n kernel-smp-net-%{_orig_name}
Linux SMP driver for the 3Com Gigabit Server BCM5700 (3c996) Network
Interface Cards.

%description -n kernel-smp-net-%{_orig_name} -l pl
Sterownik dla Linuksa do kart sieciowych gigabit ethernet BCM5700
(3c996). Obs³uguje karty o symbolach 3c996B-T i 3c996-SX.

%prep
%setup -q -n %{_orig_name}-%{version} -c

%build
cd src
%{__make} CC="%{kgcc} %{rpmcflags} -Wall -I%{_kernelsrcdir}/include -D__SMP__ -DCONFIG_X86_LOCAL_APIC"
mv -f %{_orig_name}.o ../%{_orig_name}-smp.o
%{__make} clean
%{__make} CC="%{kgcc} %{rpmcflags} -Wall -I%{_kernelsrcdir}/include"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/net
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/net/%{_orig_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net/%{_orig_name}.o
install src/%{_orig_name}.4.gz $RPM_BUILD_ROOT%{_mandir}/man4

gzip -9nf RELEASE.TXT

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/net/*
%{_mandir}/man?/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc *.gz 
/lib/modules/%{_kernel_ver}smp/net/*
%{_mandir}/man?/*
