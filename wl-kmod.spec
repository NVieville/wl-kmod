# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels current

Name:       wl-kmod
Version:    6.30.223.271
Release:    4%{?dist}
Summary:    Kernel module for Broadcom wireless devices
Group:      System Environment/Kernel
License:    Redistributable, no modification permitted
URL:        https://www.broadcom.com/support/?gid=1
Source0:    https://www.broadcom.com/docs/linux_sta/hybrid-v35-nodebug-pcoem-6_30_223_271.tar.gz
Source1:    https://www.broadcom.com/docs/linux_sta/hybrid-v35_64-nodebug-pcoem-6_30_223_271.tar.gz
Source11:   wl-kmod-kmodtool-excludekernel-filterfile
Patch0:     wl-kmod-001_wext_workaround.patch
Patch1:     wl-kmod-002_kernel_3.18_null_pointer.patch
Patch2:     wl-kmod-003_gcc_4.9_remove_TIME_DATE_macros.patch
Patch3:     wl-kmod-004_kernel_4.3_rdtscl_to_rdtsc.patch

BuildRequires:  %{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64
# ppc disabled because broadcom only provides x86 and x86_64 bits

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
These packages contain Broadcom's IEEE 802.11a/b/g/n hybrid Linux device 
driver for use with Broadcom's BCM4311-, BCM4312-, BCM4313-, BCM4321-, 
BCM4322-, BCM43142-, BCM43224-, BCM43225-, BCM43227-, BCM43228-, 
BCM4331-, BCM4360 and -BCM4352- based hardware.

NOTE: You must read the LICENSE.txt file in the docs directory before using
this software. You should read the fedora.readme file in the docs directory 
in order to know how to  configure this software if you encounter problems 
while boot sequence or with the CFG80211 API (revert to the WEXT API).

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
%ifarch %{ix86}
 tar xzf %{SOURCE0}
%else
 tar xzf %{SOURCE1}
%endif
%patch0  -p1 -b .wext_workaround.patch
%patch1  -p1 -b .kernel_3.18_null_pointer.patch
%patch2  -p1 -b .gcc_4.9_remove_TIME_DATE_macros
%patch3  -p1 -b .kernel_4.3_rdtscl_to_rdtsc.patch
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Dec 21 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.271-4
- Add patch to replace call to rdtscl with call to rdtsc for kernel >= 4.3
  thanks to Tim Thomas

* Sun Oct 18 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.271-3
- Re-add patch to remove __DATE__ and __TIME__ macros for gcc >= 4.9 in order to allow
  reproducible builds - thanks to Tim Thomas

* Sat Oct 17 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.271-2
- Re-add patch for kernel >= 3.18

* Wed Oct 14 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.271-1
- Upstream update to 6.30.223.271
- Patches cleaned-up and removed

* Tue Oct 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-9.3
- Rebuilt for kernel

* Wed Sep 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-9.2
- Rebuilt for kernel

* Wed Sep 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-9.1
- Rebuilt for kernel

* Wed Aug 26 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-9
- Add patch for 4.2 kernel

* Fri Aug 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.11
- Rebuilt for kernel

* Thu Aug 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.10
- Rebuilt for kernel

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.9
- Rebuilt for kernel

* Thu Jul 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.8
- Rebuilt for kernel

* Fri Jul 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.7
- Rebuilt for kernel

* Thu Jul 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.6
- Rebuilt for kernel

* Thu Jul 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.5
- Rebuilt for kernel

* Sun Jun 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.4
- Rebuilt for kernel

* Wed Jun 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.3
- Rebuilt for kernel

* Tue Jun 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.2
- Rebuilt for kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-8.1
- Rebuilt for kernel

* Wed May 20 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-8
- Update new Broadcom upstream URLs in SPEC file

* Wed May 20 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.10
- Rebuilt for kernel

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.9
- Rebuilt for kernel

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.8
- Rebuilt for kernel

* Sat May 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.7
- Rebuilt for kernel

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.6
- Rebuilt for kernel

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.5
- Rebuilt for kernel

* Mon Mar 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.4
- Rebuilt for kernel

* Wed Mar 25 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7.2
- Rebuilt for current

* Wed Mar 25 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-7.1
- Modified patch for kernel >= 4.0 to allow build for kernel < 4.0

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-7
- Add patch for 4.0 kernel

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.6
- Rebuilt for kernel

* Sat Mar 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.5
- Rebuilt for kernel

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.4
- Rebuilt for kernel

* Fri Mar 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.3
- Rebuilt for kernel

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.2
- Rebuilt for kernel

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-6.1
- Rebuilt for kernel

* Wed Feb 04 2015 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-6
- Added patch to fix rfbz#3533 for kernel >= 3.18

* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.6
- Rebuilt for kernel

* Wed Jan 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.5
- Rebuilt for kernel

* Thu Jan 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.4
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.3
- Rebuilt for kernel

* Fri Dec 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.2
- Rebuilt for kernel

* Sun Dec 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5.1
- Rebuilt for kernel

* Fri Dec 05 2014 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.248-5
- Rebuilt for f21 final kernel

* Mon Oct 27 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-4
- Added patch to build for kernel >= 3.18

* Fri Oct 03 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-3
- Added patch to build for kernel >= 3.17

* Wed Sep 10 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-2
- Added patch to build for kernel >= 3.16

* Tue Jul 15 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.248-1
- Upstream update to 6.30.223.248
- Patches cleaned-up and removed

* Tue Jul 08 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-8
- Added late patch for __devinit since kernel 3.8
- Modified patch to build for kernel >= 3.15

* Thu May 08 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-7
- Added patch to build with gcc >= 4.9 - fix error __TIME__ and __DATE__ macros

* Tue Apr 22 2014 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-6
- Added patch to build for kernel >= 3.15

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-5
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-4
- Rebuilt for f20 final kernel

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-3
- Rebuilt for f20 final kernel

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.30.223.141-2
- Rebuilt

* Sat Sep 14 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 6.30.223.141-1
- Upstream update to 6.30.223.141

* Wed Jul 03 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-11
- Modified patch to build for kernel >= 3.10

* Fri Mar 08 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-10
- Modified patch to build for kernel >= 3.8 rfbz#2715
- Modified patch to build for kernel >= 3.9

* Mon Mar 04 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-9
- Added patch to build for kernel >= 3.9

* Fri Mar 01 2013 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-8
- Added patch to build for kernel >= 3.8

* Wed Nov 21 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-7
- Added patch to choose API at build time (WEXT or CFG80211) to workaround #2548 #2562
- Others patches cleaned-up

* Sat Oct 20 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-6
- Added patch to include semaphore.h in wl_iw.h
- Added patch from Archlinux to disable too many "ERROR @wl_cfg80211_get_station..." messages
  in /var/log/messages since activation of CFG80211 API

* Wed Oct 17 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5.1
- Cleaned up patch for kernel >= 3.6

* Tue Oct 16 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-5
- Added patch to build for kernel >= 3.6

* Wed Oct 10 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-4.1
- Added patch to build with CFG80211 API as default for F-17

* Sun Jun 24 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3.1
- spec file cleanup

* Fri Jun 08 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-3
- Added patch to build for kernel >= 3.4

* Thu Apr 19 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2.1
- Rebuilt for Rawhide

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 5.100.82.112-2.1
- Rebuild for UsrMove

* Mon Jan 09 2012 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-2
- Added patch to build for kernel >= 3.2

* Mon Nov 07 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.112-1
- Updated version to 5.100.82.112

* Sat Nov 05 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1.1
- Rebuilt for F-16

* Fri Nov 04 2011 Nicolas Viéville <nicolas.vieville@univ-valenciennes.fr> - 5.100.82.38-1
- Updated version to 5.100.82.38

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.12
- rebuild for updated kernel

* Sun Oct 30 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.11
- rebuild for updated kernel

* Wed Oct 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.10
- rebuild for updated kernel

* Fri Oct 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.9
- rebuild for updated kernel

* Sat Sep 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.8
- rebuild for updated kernel

* Wed Aug 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.7
- rebuild for updated kernel

* Sun Jul 31 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.6
- rebuild for updated kernel

* Tue Jul 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 5.60.48.36-2.5
- Rebuild for updated kernel

* Wed Jun 15 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.4
- rebuild for updated kernel

* Sat Jun 04 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.3
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.2
- rebuild for updated kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.60.48.36-2.1
- rebuild for F15 release kernel

* Sun Sep 26 2010 Chris Nolan <chris@cenolan.com> - 5.60.48.36-2
- added patch for kernel > 2.6.33
- added multicast kernel patch
- added bogus debug_lockdep_rcu_enabled patch

* Mon Feb 22 2010 Chris Nolan <chris@cenolan.com> - 5.60.48.36-1
- Updated version to 5.60.48.36

* Tue Feb 09 2010 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-4
- added patch for linux kernel 2.6.32

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.7
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.6
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.91.9.3-3.1
- rebuild for new kernels

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-3
- fixed licence patch

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-2
- new licence patch

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9.3-1
- updated to 5.10.91.9.3

* Sat Sep 19 2009 Chris Nolan <chris@cenolan.com> - 5.10.91.9-1
- updated to 5.10.91.9

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.9
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.79.10-2.1
- rebuild for new kernels

* Sat Mar 28 2009 Chris Nolan <chris@cenolan.com> - 5.10.79.10-2
- repatched to load lib80211_crypt_tkip module - bug #466

* Sun Mar 08 2009 Chris Nolan <chris@cenolan.com> - 5.10.79.10-1
- update version to 5.10.79.10

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.14-1.2
- rebuild for latest Fedora kernel;

* Tue Feb 03 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.14-1.1
- rebuilt

* Sun Feb 01 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.14-1
- update version to 5.10.27.14
- added patch to build against 2.6.29 kernel

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.4
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.3
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.2
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.12-1.1
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.12-1
- Update version to 5.10.27.12
- Remove vlanmode and build patches

* Sun Jan 04 2009 Chris Nolan <chris@cenolan.com> - 5.10.27.11-1.2
- added patch for building on 2.6.29 kernel

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.11-1.1
- rebuild for latest Fedora kernel;

* Wed Dec 31 2008 Chris Nolan <chris@cenolan.com> 5.10.27.11-1
- Update version to 5.10.27.11

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.8
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.7
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.6
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.5
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.4
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.3
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.2
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5.10.27.6-5.1
- rebuild for latest Fedora kernel;

* Sat Nov 08 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-5
- Fixed incorrect use of /usr/src/kernels/${kernel_version%%___*}

* Sun Nov 02 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-4
- Just a spec file tidy up, nothing new

* Thu Oct 30 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-3
- Moved userland package broadcom-wl into separate package

* Mon Oct 27 2008 Chris Nolan <chris@cenolan.com> 5.10.27.6-2
- Patch to fix vlanmode issue which prevents SSH connections when the driver is used.
- Changed kmod name to wl-kmod as per convention
- Added userland package broadcom-wl which provides kmod-wl-common which contains the required license doc

* Sat Oct 25 2008 Jarod Wilson <jarod@wilsonet.com> 5.10.27.6-1
- Initial build.
