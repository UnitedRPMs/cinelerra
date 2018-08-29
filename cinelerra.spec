# Tips thanks to goodguy
# Current commit https://git.cinelerra-cv.org/gitweb?p=goodguy/cinelerra.git
%global commit0 667e703a0f3a9ba52b2a917cd8ee50a8115b27dc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           cinelerra
Version:        5.1
Release:	2%{?dist}
Summary:        A non linear video editor and effects processor
License:        GPLv2
Group:          Applications/Multimedia
Url:            http://cinelerra-cv.org/
Source0:	https://git.cinelerra-cv.org/gitweb?p=goodguy/cinelerra.git;a=snapshot;h=%{commit0};sf=tgz#/%{name}-%{shortcommit0}.tar.gz
Patch:		unblock.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libdv)
BuildRequires:  pkgconfig(mjpegtools)
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
BuildRequires:  lame-devel 
BuildRequires:  twolame-devel 
BuildRequires:  libjpeg-turbo-devel 
BuildRequires:	libsndfile-devel 
BuildRequires:  libuuid-devel 
BuildRequires:  opus-devel 
BuildRequires:  libtheora-devel 
BuildRequires:  ctags 
BuildRequires:  libtiff-devel
BuildRequires:  opencv-devel 
BuildRequires:	opencv-xfeatures2d-devel
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
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif
%if 0%{?fedora} <= 27
BuildRequires:	ladspa-devel
%endif
Recommends:	opencv-xfeatures2d
Recommends:	python2-opencv

%description
Non-linear audio/video authoring tool Cinelerra-CV is a complete audio and
video authoring tool. It understands a lot of multimedia formats as quicktime, avi, ogg 
also audio/video compression codecs divx, xvid, mpeg2. 
This is the community-maintained version of Cinelerra.


%prep
%autosetup -n %{name}-%{shortcommit0} -p1
sed -i 's/\<python\>/python2.7/' guicast/Makefile

%build

# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Quick_Opt-Out
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

export CC="gcc"
export CXX="g++"
export CFLAGS+=" -Wwrite-strings -D__STDC_CONSTANT_MACROS"
export CPPFLAGS="$CFLAGS"

autoreconf -vfi
#./autogen.sh

export FFMPEG_EXTRA_CFG=" --disable-vdpau" 
./configure --prefix=%{_prefix} \
            --with-exec-name=cinelerra \
            --with-jobs=$jobs \
            --with-opencv=sys \
            --enable-x265 \
            --enable-x264 \
            --enable-libvpx \
            --enable-fftw \
            --enable-flac \
            --enable-lame \
            --enable-opus \
%if 0%{?fedora} <= 27
            --with-ladspa-build=no 
%endif

make -j$jobs V=0

%install
make DESTDIR=%{buildroot} install V=0

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc README
%{_bindir}/cinelerra
%{_bindir}/cin_db
%{_bindir}/zmpeg3cat
%{_bindir}/zmpeg3cc2txt
%{_bindir}/zmpeg3ifochk
%{_bindir}/zmpeg3show
%{_bindir}/zmpeg3toc
%{_datadir}/cinelerra/
%{_libdir}/cinelerra/
%{_datadir}/applications/cinelerra.desktop
%{_datadir}/pixmaps/cinelerra.svg
%{_datadir}/pixmaps/cinelerra.xpm


%changelog

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

