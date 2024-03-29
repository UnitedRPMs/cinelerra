#
# spec file for package cinelerra
#
# Copyright (c) 2022 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

%define _legacy_common_support 1
%global _lto_cflags %{nil}
%undefine _hardened_build

# Tips thanks to goodguy
# Current commit https://git.cinelerra-gg.org/git/?p=goodguy/cinelerra.git;a=summary
%global commit0 c0c6e96a4ef619db6d002ecce3d799cc8da27066
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           cinelerra
Version:        5.1
Release:	17%{?dist}
Epoch:		1
Summary:        A non linear video editor and effects processor
License:        GPLv2
Group:          Applications/Multimedia
Url:            https://www.cinelerra-gg.org/
Source0:	https://git.cinelerra-gg.org/git/?p=goodguy/cinelerra.git;a=snapshot;h=%{commit0};sf=zip#/%{name}-%{shortcommit0}.tar.gz

Source1:	org.cinelerra_gg.cinelerra.metainfo.xml

#Patch:unblock.patch
Patch1:		gcc-openexr.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(libva-drm)
BuildRequires:  libmpeg2-devel >= 0.3.2
BuildRequires:  pkgconfig(xv)
BuildRequires:  faac-devel
BuildRequires:  yasm 
BuildRequires:  nasm 
BuildRequires:  cmake 
BuildRequires:  libxml2-devel  
BuildRequires:  perl-XML-LibXML 
BuildRequires:  perl-XML-Parser 
BuildRequires:  wget 
BuildRequires:  curl 
BuildRequires:  fftw-devel 
BuildRequires:  gcc-gfortran
BuildRequires:  lame-devel 
BuildRequires:  twolame-devel 
BuildRequires:  libjpeg-turbo-devel 
BuildRequires:	libsndfile-devel 
BuildRequires:  libuuid-devel 
BuildRequires:  opus-devel 
BuildRequires:  libtheora-devel 
BuildRequires:  ctags 
BuildRequires:  libtiff-devel
%if 0%{?fedora} <= 35
BuildRequires:  opencv-devel >= 4.4.0
BuildRequires:	opencv-xfeatures2d-devel >= 4.4.0
%endif
BuildRequires:	texinfo
BuildRequires:	alsa-lib-devel
BuildRequires:	ncurses-devel
BuildRequires:	udftools
BuildRequires:	libXft-devel
BuildRequires:	libXinerama-devel
BuildRequires:	xz-devel
BuildRequires:	gettext
BuildRequires:  perl-interpreter
BuildRequires:  gcc-c++
BuildRequires:	libvorbis-devel
# new
BuildRequires:	libusb-devel
BuildRequires:	esound-devel
BuildRequires:	liba52-devel
BuildRequires:	giflib-devel
%if 0%{?fedora} >= 29
BuildRequires:	python2-devel
BuildRequires:	python-unversioned-command
BuildRequires:	python2-rpm-macros
%endif
%if 0%{?fedora} <= 27
BuildRequires:	ladspa-devel
%endif
BuildRequires:	libvpx-devel
#BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(serd-0)
BuildRequires:  pkgconfig(sratom-0)
BuildRequires:  pkgconfig(suil-0)
BuildRequires:  xorg-x11-font-utils
BuildRequires:	ctags
BuildRequires:	numactl-devel
#----------------------------------------------------------------
# Enabled support for internal ffmpeg
%if 0%{?fedora} >= 34
BuildRequires:	libdav1d-devel >= 0.8.0
%else
BuildRequires:	libdav1d-devel >= 0.5.2
%endif
#BuildRequires:	xvidcore-devel
#BuildRequires:  libass-devel
#BuildRequires:  libbluray-devel
#BuildRequires:	snappy-devel
%if 0%{?fedora} >= 33
BuildRequires:  libaom-devel >= 2.0.0
%else
BuildRequires:  libaom-devel
%endif
BuildRequires:	pulseaudio-libs-devel
%if 0%{?fedora} >= 35
BuildRequires:	libpulsecommon-15.0.so
%endif
#----------------------------------------------------------------
%if 0%{?fedora} <= 35
Recommends:	opencv-xfeatures2d >= 4.4.0
Recommends:	python2-opencv >= 4.4.0
%endif

%description
Non-linear audio/video authoring tool Cinelerra-CV is a complete audio and
video authoring tool. It understands a lot of multimedia formats as quicktime, avi, ogg 
also audio/video compression codecs divx, xvid, mpeg2. 
This is the community-maintained version of Cinelerra.


%prep
%setup -n %{name}-%{shortcommit0} 

pushd cinelerra-%{version}
sed -i 's/\<python\>/python2.7/' guicast/Makefile
find -depth -type f -writable -name "*.py" -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +

pushd thirdparty/src/
tar xJf openexr-2.4.1.tar.xz -C $PWD
pushd openexr-2.4.1
%patch1 -p1
popd
tar cJf openexr-2.4.1.tar.xz openexr-2.4.1
  popd
   popd

%build
pushd cinelerra-%{version}
# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

#export CC="gcc"
#export CXX="g++"
#export CFLAGS+=" -Wwrite-strings -D__STDC_CONSTANT_MACROS"
#export CPPFLAGS="$CFLAGS"

#autoreconf -vfi
./autogen.sh

export FFMPEG_EXTRA_CFG=" --disable-doc --disable-debug --arch=%{_target_cpu} --disable-lto" 
export CFLAGS='%{optflags}'
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
# Configure uses g77 by default, if present on system
export F77=gfortran

./configure --prefix=%{_prefix} \
            --disable-dependency-tracking \
            --with-exec-name=cinelerra \
            --with-jobs=$jobs \
            --enable-x265 \
            --enable-x264 \
            --enable-flac \
            --enable-lame=auto \
            --enable-fftw=auto \
            --enable-opus \
            --enable-lv2=shared \
            --enable-lilv=shared \
            --enable-serd=shared \
            --enable-sratom=shared \
            --enable-suil=shared \
            --with-pulse \
            --with-opencv=auto 
            
#             --without-opencv \            
#--with-opencv=sta,tar=https://cinelerra-gg.org/download/opencv/opencv-20200306.tgz 

make -j$jobs V=0

%install
pushd cinelerra-%{version}
make DESTDIR=%{buildroot} install V=0

  # Metainfo
  install -Dm 0644 %{S:1} %{buildroot}/%{_metainfodir}/org.cinelerra_gg.cinelerra.metainfo.xml

%find_lang %{name}

%files -f cinelerra-%{version}/%{name}.lang 
%license cinelerra-%{version}/COPYING
%doc cinelerra-%{version}/README
%{_bindir}/bdwrite
%{_bindir}/cinelerra
%{_bindir}/zmpeg3cc2txt
%{_bindir}/zmpeg3ifochk
%{_datadir}/cinelerra/
%{_libdir}/cinelerra/
%{_datadir}/applications/cinelerra.desktop
%{_datadir}/pixmaps/cinelerra.svg
%{_datadir}/pixmaps/cinelerra.xpm
%{_metainfodir}/org.cinelerra_gg.cinelerra.metainfo.xml

%changelog

* Tue Feb 08 2022 David Va <davidva AT tuta DOT io> - 5.1-17
- Updated to current commit

* Mon Dec 14 2020 David Va <davidva AT tuta DOT io> - 5.1-16
- Updated to current commit

* Mon Sep 28 2020 David Va <davidva AT tuta DOT io> - 5.1-15
- Updated to current commit

* Fri Aug 14 2020 David Va <davidva AT tuta DOT io> - 5.1-14
- Rebuilt for opencv

* Wed Jul 08 2020 David Va <davidva AT tuta DOT io> - 5.1-13
- Rebuilt for aom
- Updated to current commit

* Mon Apr 27 2020 David Va <davidva AT tuta DOT io> - 5.1-12
- Rebuilt for opencv
- Updated to current commit
- Metainfo added

* Thu Feb 20 2020 David Va <davidva AT tuta DOT io> - 5.1-11
- Updated to current commit

* Sun Dec 29 2019 David Va <davidva AT tuta DOT io> - 5.1-10
- Rebuilt for opencv

* Sun Dec 01 2019 David Va <davidva AT tuta DOT io> - 5.1-9
- Updated to current commit

* Wed Oct 30 2019 David Va <davidva AT tuta DOT io> - 5.1-8
- Rebuilt for opencv
- Updated to current commit

* Thu Sep 05 2019 David Va <davidva AT tuta DOT io> - 5.1-7
- Updated to current commit

* Wed May 29 2019 David Va <davidva AT tuta DOT io> - 5.1-6
- Updated to current commit

* Fri May 03 2019 David Va <davidva AT tuta DOT io> - 5.1-5
- Updated to current commit
- Sources and site changed to Cinelerra Infiniy

* Thu Dec 13 2018 David Va <davidva AT tuta DOT io> - 5.1-4
- Updated to current commit

* Sun Oct 14 2018 David Va <davidva AT tuta DOT io> - 5.1-3
- Updated to current commit

* Sat Jun 16 2018 David Va <davidva AT tuta DOT io> - 5.1-2
- Updated to current commit

* Thu Jun 07 2018 David Va <davidva AT tuta DOT io> - 5.1-1
- Updated to 5.1

* Thu Feb 18 2016 Sérgio Basto <sergio@serjux.com> - 2.3-9.20160216git5aa9bc2
- Fix undefined-non-weak-symbols on libguicast.so .
- Add 0001-Do-not-ask-for-specific-Microsoft-fonts.patch is what left from
  patch: "Remove bundle fonts and fix font search path" and was not accepted
  upstream.

* Fri Jan 15 2016 Sérgio Basto <sergio@serjux.com> - 2.3-8.20160216git5aa9bc2
- AutoTools replace the obsoleted AC_PROG_LIBTOOL, patch7.
- To fix hardened linkage, patch8.
- More reviews like replace RPM_BUILD_ROOT, own directories, more documentation,
  description-line-too-long errors.

* Thu Jan 14 2016 Sérgio Basto <sergio@serjux.com> - 2.3-7.20160114git454be60
- Update license tag.
- Add license macro.
- use macro make_build .
- use macro make_install .
- Improve conditional builds.

* Mon Oct 26 2015 Sérgio Basto <sergio@serjux.com> - 2.3-6.20151026git99d2887
- Update to git 99d2887, drop cinelerra-cv-remove-fonts.patch is was applied upstream.

* Mon Oct 05 2015 Sérgio Basto <sergio@serjux.com> - 2.3-5.20151005gitd189a04
- Update to git d189a04

* Tue Sep 29 2015 Sérgio Basto <sergio@serjux.com> - 2.3-4.20150929git2c849c6
- Drop upstreamed cinelerra-cv-intltoolize.patch

* Tue Sep 15 2015 Sérgio Basto <sergio@serjux.com> - 2.3-3.20150912gitc25d3b1
- Applied cinelerra-cv-intltoolize.patch

* Mon Sep 14 2015 Sérgio Basto <sergio@serjux.com> - 2.3-2.20150912gitc25d3b1
- Enabled findobject plugin using OpenCV 2.0 .
- Fix unknown freetype2 option, an configure warning.

* Sun Sep 13 2015 Sérgio Basto <sergio@serjux.com> - 2.3-1.20150912gitc25d3b1
- Update cinelerra-cv to 2.3 more a few commits.

* Wed Dec 24 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.9.20141224git70b8c14
- Update to 20141224git70b8c14

* Sun Oct 12 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1.20141012git623e87e-1
- Update to git623e87e

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.8.20140927git9cbf7f0
- Update to cinelerra-cv-2.2.1-20140927git9cbf7f0

* Sun Jul 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.7.20140727git92dba16
- Update to 20140727 git 92dba16 .

* Sun May 25 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.5.20140525gitef4fddb
- Update to git ef4fddb
- Added cinelerra-cv-ffmpeg_api2.2.patch and cinelerra-cv-ffmpeg2.0.patch and build with external ffmpeg.
- make it work --with or --without libmpeg3_system and ffmpeg_system.

* Wed Apr 30 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.3.20140426git9154825
- Added imlib2-devel as BR to build vhook/imlib2.so

* Tue Apr 29 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.2.20140426git9154825
- Drop a file in /etc/sysctl.d instead to tweaking /etc/sysctl.conf
- Removed gcc-g++ as BR
- Use libmpeg3 from system
- Remove bundle fonts and fix font search path
- Scriptlet for desktop-database
- Disabled 3dnow
- Program-suffix -cv

* Mon Apr 28 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.1
- Initial spec, copied from David Vasquez and changed based on
  cinelerra-f15.spec from Atrpms and also changed based on
  openmamba/devel/specs/cinelerra-cv.spec

* Mon Sep 30 2013 David Vasquez <davidjeremias82@gmail.com> - 2.2-1
- Initial package creation for Fedora 19
- Spec inspirated in PKGBUILD Arch Linux
- Add freeing more shared memory from RPM Fusion

