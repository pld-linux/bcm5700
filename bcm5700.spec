#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
%define		_orig_name	bcm5700

Summary:	Linux driver for the 3Com Gigabit Server BCM5700 (3c996) Network Interface Cards
Summary(pl):	Sterownik dla Linuksa do kart sieciowych gigabit ethernet BCM5700 (3c996)
Name:		kernel-net-%{_orig_name}
Version:	2.2.27
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://support.3com.com/infodeli/tools/nic/linux/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	9aa1e1b2183675df8e1cfd2974ca6a2e
URL:		http://support.3com.com/infodeli/tools/nic/linuxdownload.htm
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
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
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

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
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o
install src/%{_orig_name}.4.gz $RPM_BUILD_ROOT%{_mandir}/man4

%clean 
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc RELEASE.TXT
/lib/modules/%{_kernel_ver}/misc/*
%{_mandir}/man?/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc RELEASE.TXT 
/lib/modules/%{_kernel_ver}smp/misc/*
%{_mandir}/man?/*
