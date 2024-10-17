%define jogl_version	1.1.1
%define gluegen_version	1.0b06a


Summary:	Java bindings for the OpenGL API
Name:		jogl_cg
Version:	%{jogl_version}
Release:	1
Group:		Development/Java
License:	BSD
URL:		https://jogl.dev.java.net/
# svn co https://svn.java.net/svn/jogl~svn/branches/1.x-maint jogl-1.1.1
Source0:	jogl-%{jogl_version}.tar.bz2
# match gluegen package
# svn co https://svn.java.net/svn/gluegen~svn/branches/1.0b06-maint gluegen-1.0b06
Source1:	gluegen-1.0b06.tar.bz2
Source2:	jogl.properties
Patch0:		jogl-1.1.1-src-no-link-against-sun-java.patch
Patch1:		jogl-1.1.1-nvidia.patch
BuildRequires:	ant
BuildRequires:	ant-antlr
BuildRequires:	antlr
BuildRequires:	jpackage-utils
BuildRequires:	mesa-common-devel
BuildRequires:	java-rpmbuild
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
BuildRequires:	cpptasks
BuildRequires:	libcg cg-devel
Requires:	java >= 1.5
Provides:	gluegen = %{gluegen_version}
Provides:	jogl = %{jogl_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
The JOGL Project hosts a reference implementation of the Java bindings for
OpenGL API, and is designed to provide hardware-supported 3D graphics to
applications written in the Java programming language.

It is part of a suite of open-source technologies initiated bu the Game
Technology Group at Sun Microsystems.

JOGL provides full access to the APIs in the OpenGL 1.5 specification as
well as nearly all vendor extensions, and integrated with the AWT and Swing
widget sets.

%prep
%setup -q -n jogl-%{jogl_version} -b 1
ln -sf gluegen-1.0b06 ../gluegen
pushd make
%patch0 -p0
popd
%patch1 -p1
perl -pi -e 's|\@libdir\@|%{_libdir}|;'		\
    src/classes/com/sun/opengl/impl/x11/DRIHack.java

%__cp %{SOURCE2} make

%build
export OPT_JAR_LIST="antlr ant/antlr"
export CLASSPATH=$(build-classpath antlr ant/ant-antlr)

pushd make
    perl -pi -e 's@/usr/X11R6/%{_lib}@%{_libdir}@g' build.xml
    %ant					\
	-Duser.home=%{_topdir}/SOURCES		\
	-Dantlr.jar=$(build-classpath antlr)	\
	-Djogl.cg=1				\
	-Dx11.cg.lib=%{_libdir} 		\
	all
popd

pushd ../gluegen/make
    %ant					\
	-Duser.home=%{_topdir}/SOURCES		\
	-Dantlr.jar=$(build-classpath antlr)	\
	-Djogl.cg=1				\
	-Dx11.cg.lib=%{_libdir}			\
	all

%install
rm -rf %{buildroot}

# jars
%__install -dm 755 %{buildroot}%{_javadir}
%__install -m 644 build/jogl.jar				\
	%{buildroot}%{_javadir}/jogl-%{jogl_version}.jar
%__install -m 644 ../gluegen/build/gluegen.jar			\
	%{buildroot}%{_javadir}/gluegen-%{gluegen_version}.jar
%__install -m 644 ../gluegen/build/gluegen-rt.jar		\
	%{buildroot}%{_javadir}/gluegen-rt-%{gluegen_version}.jar

pushd %{buildroot}%{_javadir}
    for jar in jogl-%{jogl_version}*; do
	ln -sf ${jar} `echo $jar| sed "s|-%{jogl_version}||g"`
    done
    for jar in gluegen-*%{gluegen_version}*; do
	ln -sf ${jar} `echo $jar| sed "s|-%{gluegen_version}||g"`
    done
popd

# native lib
%__install -dm 755 %{buildroot}%{_libdir}
%__install -m 644 build/obj/lib*.so %{buildroot}%{_libdir}
%__install -m 644 ../gluegen/build/obj/lib*.so %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%attr(755,root,root) %{_libdir}/lib*.so
