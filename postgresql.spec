%define __noautoreq devel\\(libtcl)

%define _disable_lto 1

%define major 5
%define oldmajor_ecpg 7
%define major_ecpg 6
%define oldlibname %mklibname pq 5
%define libname %mklibname pq
%define libecpg %mklibname ecpg
%define veryoldlibecpg %mklibname ecpg 7
%define oldlibecpg %mklibname ecpg 6

%define majorversion %(echo %{version} | cut -d. -f1)
%define minorversion %(echo %{version} | cut -d. -f2)
%define server %{name}-server
%define contrib %{name}-contrib
%define metapl %{name}-pl
%define plpython %{name}-plpython
%define plperl %{name}-plperl
%define pltcl %{name}-pltcl
%define plpgsql %{name}-plpgsql

%define pgdata /var/lib/pgsql
%define pguser postgres
%define logrotatedir %{_sysconfdir}/logrotate.d

%bcond_without uuid

#define beta rc1
%define fsversion %{version}%{?beta:%{beta}}
# For versions tagged x.y.0: %(echo %{version} |sed -e 's,\.0$,,')%{beta}

Summary:	PostgreSQL client programs and libraries
Name:		postgresql
Version:	18.1
Release:	%{?beta:0.%{beta}.}1
License:	BSD
Group:		Databases
URL:		https://www.postgresql.org/ 
Source0:	http://ftp.postgresql.org/pub/source/v%{fsversion}/postgresql-%{fsversion}.tar.bz2
Source10:	postgres.profile
Source11:	postgresql.service
Source12:	postgresql.tmpfiles.d
Source14:	postgresql_initdb.sh

Source100:	%name.rpmlintrc
Patch1:		postgresql-run-socket.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pam-devel
BuildRequires:	perl(ExtUtils::Embed)
BuildRequires:	pkgconfig(python3)
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	rpm-helper
BuildRequires:	systemd
BuildRequires:	gettext-devel
%if %{with uuid}
BuildRequires:	ossp-uuid-devel >= 1.6.2-5
%endif
# Need to build doc
BuildRequires:	locales-extra-charsets
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-dtd42-sgml
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	openjade
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libnsl)
BuildRequires:	docbook-utils
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl

Provides:	postgresql-clients = %{version}-%{release}
#Requires:	perl

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS)
that supports almost all SQL constructs (including transactions, subselects and
user-defined types and functions). The postgresql package includes the client
programs and libraries that you'll need to access a PostgreSQL DBMS server.
These PostgreSQL client programs are programs that directly manipulate the
internal structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL server, or may
be on a remote machine which accesses a PostgreSQL server over a network
connection. This package contains the client libraries for C and C++, as well
as command-line utilities for managing PostgreSQL databases on a PostgreSQL
server.

If you want to manipulate a PostgreSQL database on a remote PostgreSQL server,
you need this package. You also need to install this package if you're
installing the postgresql-server package.

%package -n %{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Provides:	postgresql-libs = %{version}-%{release}
%rename	%{oldlibname}

%description -n %{libname}
C and C++ libraries to enable user programs to communicate with the PostgreSQL
database backend. The backend can be on another machine and accessed through
TCP/IP.

%package -n %{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
%rename %{oldlibecpg}
%rename %{veryoldlibecpg}
Conflicts:	%{mklibname ecpg 5}

%description -n %{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C) Use
postgresql-dev to develop such programs.

%package -n %{server}
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Provides:	postgresql-server = %{version}-%{release}
# add/remove services
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
# add/del user
Requires(pre,postun):	rpm-helper
Requires(post,preun):	chkconfig
# the client bins are needed for upgrading
Requires:	postgresql >= %{version}-%{release}
Requires:	postgresql-plpgsql >= %{version}-%{release}

%description -n %{server}
The postgresql-server package includes the programs needed to create and run a
PostgreSQL server, which will in turn allow you to create and maintain
PostgreSQL databases.  PostgreSQL is an advanced Object-Relational database
management system (DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). You should
install postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need to
install the postgresql and postgresql-devel packages.

%package docs
Summary:	Extra documentation for PostgreSQL
Group:		Databases

%description docs
The postgresql-docs package includes the SGML source for the documentation as
well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package -n %{contrib}
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
#Requires:	postgresql-server >= %{version}-%{release}

%description -n %{contrib}
The postgresql-contrib package includes the contrib tree distributed with the
PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libecpg} >= %{version}-%{release}

%description devel
The postgresql-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with a PostgreSQL
database management server and the ecpg Embedded C Postgres preprocessor. You
need to install this package if you want to develop applications which will
interact with a PostgreSQL server. If you're installing postgresql-server, you
need to install this package.

%package -n %{metapl}
Summary:	Procedurals languages for PostgreSQL
Group:		Databases
Provides:	%{name}-pl = %{version}-%{release}
Requires:	%{name}-plpython >= %{version}-%{release} 
Requires:	%{name}-plperl >= %{version}-%{release} 
Requires:	%{name}-pltcl >= %{version}-%{release} 
Requires:	%{name}-plpgsql >= %{version}-%{release} 

%description -n %{metapl}
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pl will install the the PL/Perl, PL/Tcl, and PL/Python procedural
languages for the backend. PL/Pgsql is part of the core server package.

%package -n %{plpython}
Summary:	The PL/Python procedural language for PostgreSQL
Group:		Databases
Provides:	%{name}-plpython = %{version}-%{release}
#Requires:	postgresql-server >= %{version}

%description -n %{plpython}
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpython package contains the the PL/Python procedural languages for
the backend. PL/Python is part of the core server package.

%package -n %{plperl}
Summary:	The PL/Perl procedural language for PostgreSQL
Group:		Databases	
Provides:	%{name}-plperl = %{version}-%{release}
#Requires:	postgresql-server >= %{version}

%description -n %{plperl}
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plperl package contains the the PL/Perl procedural languages for the
backend. PL/Perl is part of the core server package.

%package -n %{pltcl}
Summary:	The PL/Tcl procedural language for PostgreSQL
Group:		Databases
Provides:	%{name}-pltcl = %{version}-%{release}
#Requires:	postgresql-server >= %{version}

%description -n %{pltcl}
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pltcl package contains the the PL/Tcl procedural languages for the
backend. PL/Tcl is part of the core server package.

%package -n %{plpgsql}
Summary:	The PL/PgSQL procedural language for PostgreSQL
Group:		Databases
Provides:	%{name}-plpgsql = %{version}-%{release}
#Requires:	postgresql-server >= %{version}

%description -n %{plpgsql}
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpgsql package contains the the PL/PgSQL procedural languages for
the backend. PL/PgSQL is part of the core server package.

%prep
%autosetup -p1 -n postgresql-%{fsversion}

%build
%setup_compile_flags

%ifarch %{ix86}
# As of postgresql 11.0-beta2 and clang 7.0-338892,
# building with clang on i686 causes a test failure in
# the float8 test.
# Get rid of gcc use once that's fixed.
CC=gcc CXX=g++ \
%endif
%configure \
    --disable-rpath \
    --with-perl \
    --with-python \
    --with-tcl \
    --with-tclconfig=%{_libdir} \
    --with-openssl \
    --with-pam \
    --with-libxml \
%ifarch riscv64
    --disable-spinlocks \
%endif
    --with-libxslt \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/pgsql \
    --enable-nls \
%if %{with uuid}
    --with-uuid=ossp \
    --with-includes=%{_includedir}/ossp-uuid
%endif

# $(rpathdir) come from Makefile
#perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,\$(rpathdir),-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile

# nuke -Wl,--no-undefined
perl -pi -e "s|-Wl,--no-undefined||g" src/Makefile.global

%if %{with uuid}
# bork...
echo "#define HAVE_OSSP_UUID_H 1" >> src/include/pg_config.h
%endif

# python_libspec incorrectly uses the static python lib causing failures due to lto
# in any case we should use the shared one
%make_build world

pushd src/test
make all
popd

%check
make check

%install
make DESTDIR=%{buildroot} install-world install-docs

# install odbcinst.ini
mkdir -p %{buildroot}%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
#install -m755 src/Makefile.global %{buildroot}%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}%{pgdata}/data

# backups of data go here...
install -d -m 700 %{buildroot}%{pgdata}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql

# install systemd units
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}.service

# Create the directory for sockets.
install -d -m 755 %{buildroot}/run/postgresql

# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE12} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# install helper script for env initialisation 
mkdir -p %{buildroot}%{_libexecdir}
sed -e 's,@PGDIR@,%{pgdata},g' %{S:14} >%{buildroot}%{_libexecdir}/postgresql_initdb.sh
chmod 0755 %{buildroot}%{_libexecdir}/postgresql_initdb.sh

# Create the user and group
mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/postgresql.conf <<EOF
u %{pguser} 105 "PostgreSQL" %{pgdata} %{_bindir}/sh
EOF

%if 0
# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p %{buildroot}%{_libdir}/pgsql/test
cp -a src/test/regress %{buildroot}%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so %{buildroot}%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so %{buildroot}%{_libdir}/pgsql/test/regress
pushd  %{buildroot}%{_libdir}/pgsql/test/regress/
strip *.so
popd
%endif

mkdir -p %{buildroot}/var/log/postgres

mkdir -p %{buildroot}%logrotatedir
cat > %{buildroot}%logrotatedir/%{name} <<EOF
/var/log/postgres/postgresql {
    notifempty
    missingok
    copytruncate
}
EOF

mv %{buildroot}%{_docdir}/%{name}/html %{buildroot}%{_docdir}/%{name}-docs-%{version}

echo -n "" > %{libname}.lst
echo -n "" > %{libecpg}.lst
echo -n "" > server.lst
echo -n "" > main.lst
echo -n "" > devel.lst
echo -n "" > plperl.lst
echo -n "" > plpython.lst
echo -n "" > pltcl.lst
echo -n "" > plpgsql.lst

# libs
%find_lang libpq%{major}-%{majorversion}
cat libpq%{major}-%{majorversion}.lang >> %{libname}.lst
%find_lang ecpglib%{major_ecpg}-%{majorversion}
cat ecpglib%{major_ecpg}-%{majorversion}.lang >> %{libecpg}.lst

# server
%find_lang initdb-%{majorversion}
cat initdb-%{majorversion}.lang >> server.lst
%find_lang pg_basebackup-%{majorversion}
cat pg_basebackup-%{majorversion}.lang >> server.lst
%find_lang pg_controldata-%{majorversion}
cat pg_controldata-%{majorversion}.lang >> server.lst
%find_lang pg_ctl-%{majorversion}
cat pg_ctl-%{majorversion}.lang >> server.lst
%find_lang postgres-%{majorversion}
cat postgres-%{majorversion}.lang >> server.lst
%find_lang pg_rewind-%{majorversion}
cat pg_rewind-%{majorversion}.lang >>server.lst
%find_lang pg_archivecleanup-%{majorversion}
cat pg_archivecleanup-%{majorversion}.lang >>server.lst
%find_lang pg_upgrade-%{majorversion}
cat pg_upgrade-%{majorversion}.lang >>server.lst

# main
%find_lang pg_config-%{majorversion}
cat pg_config-%{majorversion}.lang >> main.lst
%find_lang pg_dump-%{majorversion}
cat pg_dump-%{majorversion}.lang >> main.lst
%find_lang pgscripts-%{majorversion}
cat pgscripts-%{majorversion}.lang >> main.lst
%find_lang psql-%{majorversion}
cat psql-%{majorversion}.lang >>main.lst
%find_lang pg_checksums-%{majorversion}
cat pg_checksums-%{majorversion}.lang >>main.lst

%find_lang pg_resetwal-%{majorversion}
cat pg_resetwal-%{majorversion}.lang >>main.lst
%find_lang pg_test_fsync-%{majorversion}
cat pg_test_fsync-%{majorversion}.lang >>main.lst
%find_lang pg_test_timing-%{majorversion}
cat pg_test_timing-%{majorversion}.lang >>main.lst
%find_lang pg_waldump-%{majorversion}
cat pg_waldump-%{majorversion}.lang >>main.lst
%find_lang pg_verifybackup-%{majorversion}
cat pg_verifybackup-%{majorversion}.lang >>main.lst
%find_lang pg_combinebackup-%{majorversion}
cat pg_combinebackup-%{majorversion}.lang >>main.lst
%find_lang pg_walsummary-%{majorversion}
cat pg_walsummary-%{majorversion}.lang >>main.lst

# contrib
%find_lang pg_amcheck-%{majorversion}
cat pg_amcheck-%{majorversion}.lang >>contrib.lst

# devel
%find_lang ecpg-%{majorversion}
cat ecpg-%{majorversion}.lang >> devel.lst

# perl
%find_lang plperl-%{majorversion}
cat plperl-%{majorversion}.lang >> plperl.lst

# python
%find_lang plpython-%{majorversion}
cat plpython-%{majorversion}.lang >> plpython.lst

# tcl
%find_lang pltcl-%{majorversion}
cat pltcl-%{majorversion}.lang >> pltcl.lst

# plpgsql
%find_lang plpgsql-%{majorversion}
cat plpgsql-%{majorversion}.lang >> plpgsql.lst

# taken directly in build dir.
rm -fr %{buildroot}%{_datadir}/doc/postgresql/contrib/

mkdir -p %{buildroot}/%_sys_macros_dir
cat > %{buildroot}/%_sys_macros_dir/%{name}.macros <<EOF
%%postgresql_version %{version}
%%postgresql_major   %{majorversion}
%%postgresql_minor   %{minorversion}
%%pgmodules_req Requires: %{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{majorversion}
EOF

# postgres' .profile and .bashrc
install -D -m 700 %SOURCE10 %{buildroot}%{pgdata}/.profile
(
cd %{buildroot}%{pgdata}/
ln -s .profile .bashrc
)

cat > %{buildroot}%_sysconfdir/sysconfig/postgresql <<EOF
# Olivier Thauvin <nanardon@mandriva.org>

# The database location:
# You probably won't change this
# PGDATA=%{pgdata}/data

# What is the based locales for postgresql
# Setting locales to C allow to use any encoding
# ISO or UTF, any other choice will restrict you
# either ISO or UTF.
LC_ALL=C

# These are additional to pass to pg_ctl when starting/restarting postgresql.
# PGOPTIONS=
EOF

# cleanup
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
find %{buildroot} -type f -name "*.a" -exec rm -f {} ';'

%files -f main.lst
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT HISTORY
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/pg_checksums
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_receivewal
%{_bindir}/pg_recvlogical
%{_bindir}/pg_restore
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_verifybackup
%{_bindir}/pg_waldump
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_bindir}/pg_combinebackup
%{_bindir}/pg_createsubscriber
%{_bindir}/pg_walsummary
%{_datadir}/postgresql
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_checksums.1*
%{_mandir}/man1/pg_combinebackup.1*
%{_mandir}/man1/pg_createsubscriber.1*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_isready.1*
%{_mandir}/man1/pg_receivewal.1*
%{_mandir}/man1/pg_recvlogical.1*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/pg_test_fsync.1*
%{_mandir}/man1/pg_test_timing.1*
%{_mandir}/man1/pg_waldump.1*
%{_mandir}/man1/pg_walsummary.1*
%{_mandir}/man1/pg_verifybackup.1*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%_sys_macros_dir/%{name}.macros

%files -n %{libname} -f %{libname}.lst
%{_libdir}/libpq.so.%{major}*

%files -n %{libecpg} -f %{libecpg}.lst
%{_libdir}/libecpg.so.%{major_ecpg}*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files docs
%doc %{_docdir}/%{name}-docs-%{version}
%{_docdir}/%{name}/extension

%files -n %{contrib} -f contrib.lst
%{_libdir}/postgresql/pg_surgery.so
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/amcheck.so
%{_libdir}/postgresql/bloom.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/cube.so
%{_libdir}/postgresql/dblink.so
%{_libdir}/postgresql/earthdistance.so
%{_libdir}/postgresql/fuzzystrmatch.so
%{_libdir}/postgresql/insert_username.so
%{_libdir}/postgresql/lo.so
%{_libdir}/postgresql/ltree.so
%{_libdir}/postgresql/moddatetime.so
%{_libdir}/postgresql/pgcrypto.so
%{_libdir}/postgresql/pgstattuple.so
%{_libdir}/postgresql/refint.so
%{_libdir}/postgresql/seg.so
%{_libdir}/postgresql/tablefunc.so
%{_libdir}/postgresql/tcn.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/isn.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pg_prewarm.so
%{_libdir}/postgresql/pg_visibility.so
%{_libdir}/postgresql/pg_logicalinspect.so
%{_libdir}/postgresql/pg_overexplain.so
%{_libdir}/postgresql/pgoutput.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/pageinspect.so
%{_libdir}/postgresql/postgres_fdw.so
%{_libdir}/postgresql/jsonb_plperl.so
%{_libdir}/postgresql/jsonb_plpython3.so
# Mostly sample code
# https://docs.postgresql.fr/15/basic-archive.html
%{_libdir}/postgresql/basic_archive.so
# Get WAL dumps, mostly for debugging
# https://www.postgresql.org/message-id/CALj2ACUGUYXsEQdKhEdsBzhGEyF3xggvLdD8C0VT72TNEfOiog@mail.gmail.com
%{_libdir}/postgresql/pg_walinspect.so
%{_bindir}/pg_amcheck
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo
%{_mandir}/man1/oid2name.1*
%{_mandir}/man1/pg_amcheck.1*
%{_mandir}/man1/pgbench.1*
%{_mandir}/man1/vacuumlo.1*

%files -n %{server} -f server.lst
%{_sysusersdir}/postgresql.conf
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%{_bindir}/initdb
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetwal
%{_bindir}/postgres
%{_bindir}/pg_rewind
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_upgrade
%{_prefix}/libexec/postgresql_initdb.sh
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetwal.*
%{_mandir}/man1/pg_rewind.*
%{_mandir}/man1/pg_upgrade.1*
%{_mandir}/man1/postgres.1*
%dir %{_libdir}/postgresql
%dir %{_datadir}/postgresql
%config(noreplace) %attr(-,%{pguser},%{pguser}) %{pgdata}/.profile
%config(noreplace) %{pgdata}/.bashrc
%attr(700,%{pguser},%{pguser}) %dir %{pgdata}
%attr(-,%{pguser},%{pguser}) %{pgdata}/data
%attr(700,%{pguser},%{pguser}) %dir %{pgdata}/backups
%{_libdir}/postgresql/*_and_*.so
%{_libdir}/postgresql/auth_delay.so
%{_libdir}/postgresql/auto_explain.so
%{_libdir}/postgresql/btree_gin.so
%{_libdir}/postgresql/citext.so
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/euc2004_sjis2004.so
%{_libdir}/postgresql/file_fdw.so
%{_libdir}/postgresql/libpqwalreceiver.so
%{_libdir}/postgresql/passwordcheck.so
%{_libdir}/postgresql/pg_stat_statements.so
%{_libdir}/postgresql/pgxml.so
%{_libdir}/postgresql/test_decoding.so
%{_libdir}/postgresql/tsm_system_rows.so
%{_libdir}/postgresql/tsm_system_time.so
%{_libdir}/postgresql/unaccent.so
%if %{with uuid}
%{_libdir}/postgresql/uuid-ossp.so
%endif
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/timezone
%{_datadir}/postgresql/system_views.sql
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt
%dir %{_datadir}/postgresql/timezonesets
%{_datadir}/postgresql/timezonesets/Africa.txt
%{_datadir}/postgresql/timezonesets/America.txt
%{_datadir}/postgresql/timezonesets/Antarctica.txt
%{_datadir}/postgresql/timezonesets/Asia.txt
%{_datadir}/postgresql/timezonesets/Atlantic.txt
%{_datadir}/postgresql/timezonesets/Australia
%{_datadir}/postgresql/timezonesets/Australia.txt
%{_datadir}/postgresql/timezonesets/Default
%{_datadir}/postgresql/timezonesets/Etc.txt
%{_datadir}/postgresql/timezonesets/Europe.txt
%{_datadir}/postgresql/timezonesets/India
%{_datadir}/postgresql/timezonesets/Indian.txt
%{_datadir}/postgresql/timezonesets/Pacific.txt
%{_datadir}/postgresql/tsearch_data
%dir %{_datadir}/postgresql/extension
%{_datadir}/postgresql/extension/*
%attr(700,postgres,postgres) %dir /var/log/postgres
%logrotatedir/%{name}
%{_mandir}/man1/pg_archivecleanup.1*
# basebackup -- https://www.postgresql.org/docs/current/app-pgbasebackup.html
# Keep in main, or subpackage?
%{_bindir}/pg_basebackup
%{_mandir}/man1/pg_basebackup.*
%{_libdir}/postgresql/basebackup_to_shell.so

%files devel -f devel.lst
# %doc doc/TODO doc/TODO.detail
%{_includedir}/*
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg.so
%{_libdir}/libpgtypes.so
%{_libdir}/libpq.so
%{_libdir}/postgresql/pgxs/
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/ecpg.1*
%{_mandir}/man1/pg_config.1*
%{_mandir}/man3/SPI_*.3*
%{_mandir}/man3/dblink*.3*

%files -n %{metapl}
# metapkg

%files -n %{plpython} -f plpython.lst
%{_libdir}/postgresql/hstore_plpython3.so
%{_libdir}/postgresql/plpython*.so
%{_libdir}/postgresql/ltree_plpython3.so

%files -n %{plperl} -f plperl.lst
%{_libdir}/postgresql/hstore_plperl.so
%{_libdir}/postgresql/plperl.so
%{_libdir}/postgresql/bool_plperl.so

%files -n %{pltcl} -f pltcl.lst
%{_libdir}/postgresql/pltcl.so

%files -n %{plpgsql} -f plpgsql.lst
%{_libdir}/postgresql/plpgsql.so

%pretrans server
# Postgres major updates usually require a full dump and restore...
OLDMAJOR="$(pg_dumpall --version 2>/dev/null |cut -d' ' -f3 |cut -d. -f1)"
if [ -n "$OLDMAJOR" -a "0$OLDMAJOR" -lt %{majorversion} ]; then
	echo "This is a major update from $OLDMAJOR to %{majorversion}"
	if [ "$OLDMAJOR" -le 16 ]; then
		OLDSERVICE=postgresql$OLDMAJOR
	else
		OLDSERVICE=postgresql
	fi
	UPDIR="%{pgdata}/update-from-$OLDMAJOR-to-%{majorversion}"
	mkdir -p "$UPDIR"
	chown postgres:postgres "$UPDIR"
	if systemctl is-enabled $OLDSERVICE &>/dev/null; then
		touch "$UPDIR/.was-enabled"
	fi
	if systemctl is-active $OLDSERVICE &>/dev/null; then
		touch "$UPDIR/.was-running"
	else
		systemctl start $OLDSERVICE
	fi
	su - postgres -c "pg_dumpall -w -f $UPDIR/db.dump --quote-all-identifiers" &>$UPDIR/dump.log
	systemctl stop $OLDSERVICE
	mv %{pgdata}/data %{pgdata}/data-from-$OLDMAJOR
fi

%posttrans server
if [ -d %{pgdata}/data-from-%{majorversion} ]; then
	cat >&2 <<"EOF"
You seem to be undoing an update.
Moving the matching database files back in place.
EOF
	[ -d %{pgdata}/data ] && mv %{pgdata}/data %{pgdata}/data-failed-update
	mv %{pgdata}/data-from-%{majorversion} %{pgdata}/data
fi
# Upgrading is handled in postgresql_initdb.sh on next startup
UPDIR="$(ls -1d %{pgdata}/update-from-*-to-%{majorversion} |head -n1 2>/dev/null)"
if [ -e "$UPDIR/.was-enabled" ]; then
	systemctl enable --now postgresql
elif [ -e "$UPDIR/.was-running" ]; then
	systemctl start postgresql
fi
