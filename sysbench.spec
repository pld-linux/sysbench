%bcond_without	tests
Summary:	a system performance benchmark
Name:		sysbench
Version:	1.0.20
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/akopytov/sysbench/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	756381c6fc4e16af1e0831b5e6a3dcb3
Patch0:		%{name}-1.0.20-fix_deprecated_egrep_call.patch
Patch1:		%{name}-1.0.20-python3.patch
URL:		https://github.com/akopytov/sysbench/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libaio-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	luajit-devel
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
%patch0 -p1
%patch1 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+bash(\s|$),#!/bin/bash\1,' \
      tests/include/drv_common.sh \
      tests/include/script_bulk_insert_common.sh \
      tests/include/script_oltp_common.sh \
      tests/include/script_oltp_legacy_common.sh \
      tests/include/script_select_random_common.sh \
      tests/include/script_select_random_legacy_common.sh \
      tests/test_run.sh

%{__sed} -E -i -e '1s,#!\s*%{_bindir}/env\s+sysbench(\s|$),#!%{_bindir}/sysbench\1,' \
	src/lua/bulk_insert.lua \
	src/lua/oltp_delete.lua \
	src/lua/oltp_insert.lua \
	src/lua/oltp_point_select.lua \
	src/lua/oltp_read_only.lua \
	src/lua/oltp_read_write.lua \
	src/lua/oltp_update_index.lua \
	src/lua/oltp_update_non_index.lua \
	src/lua/oltp_write_only.lua \
	src/lua/select_random_points.lua \
	src/lua/select_random_ranges.lua

rm -r third_party/luajit/luajit/
#rm -r third_party/concurrency_kit/ck/
#rm -r third_party/cram/

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-mysql \
	--with-pgsql \
	--with-system-luajit \
	--without-gcc-arch \
	--disable-silent-rules
# --with-system-ck
%{__make}

%if %{with tests}
cd tests
./test_run.sh
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_docdir}/sysbench/manual.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md doc/manual.html
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/sysbench
