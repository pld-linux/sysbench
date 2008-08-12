Summary:	a system performance benchmark
Name:		sysbench
Version:	0.4.8
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/sysbench/%{name}-%{version}.tar.gz
# Source0-md5:	da17b9654ec7cb8ebc0b8a8062a41dce
URL:		http://sysbench.sourceforge.net/
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SysBench is a modular, cross-platform and multi-threaded benchmark
tool for evaluating OS parameters that are important for a system
running a database under intensive load.

The idea of this benchmark suite is to quickly get an impression about
system performance without setting up complex database benchmarks or
even without installing a database at all. Current features allow to
test the following system parameters:
- file I/O performance
- scheduler performance
- memory allocation and transfer speed
- POSIX threads implementation performance
- database server performance (OLTP benchmark)

Primarily written for MySQL server benchmarking, SysBench will be
further extended to support multiple database backends, distributed
benchmarks and third-party plug-in modules.

%prep
%setup -q

%build
%configure \
	--with-mysql \
	--with-pgsql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO doc/manual.html
%attr(755,root,root) %{_bindir}/s*