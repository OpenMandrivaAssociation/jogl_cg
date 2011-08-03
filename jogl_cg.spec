Summary:	Java bindings for the OpenGL API
Name:		jogl
Version:	1.1.1
Release:	%mkrel 0.6.9
Group:		Development/Java
License:	BSD
URL:		http://jogl.dev.java.net/
# svn co https://svn.java.net/svn/jogl~svn/branches/1.x-maint jogl-1.1.1
Source0:	%{name}-%{version}.tar.bz2
# match gluegen package
# svn co https://svn.java.net/svn/gluegen~svn/branches/1.0b06-maint gluegen-1.0b06
Source1:	gluegen-1.0b06.tar.bz2
Patch0:		%{name}-1.1.1-src-no-link-against-sun-java.patch
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
Conflicts:	gluegen
Conflicts:	jogl
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
%setup -q -b 1
ln -sf gluegen-1.0b06 ../gluegen
pushd make
%patch0 -p0
popd

%__cp %{SOURCE1} make

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
%__install -m 644 build/%{name}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
popd

# native lib
%__install -dm 755 %{buildroot}%{_libdir}
%__install -m 644 build/obj/lib*.so \
	%{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%attr(755,root,root) %{_libdir}/lib*.so
