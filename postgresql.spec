%define _requires_exceptions devel(libtcl

# %%define Werror_cflags %nil
# %%define _disable_ld_no_undefined 1

%define perl_version %(rpm -q --qf "%{VERSION}" perl)
%define perl_epoch %(rpm -q --qf "%{EPOCH}" perl)

%define pgdata /var/lib/pgsql
%define logrotatedir %{_sysconfdir}/logrotate.d

%define major 5
%define major_ecpg 6
%define libname %mklibname pq %{major}
%define libecpg %mklibname ecpg %{major_ecpg}

%define current_major_version 9.1
%define current_minor_version 1

%define withuuid 0
%if %mdvver >= 201100
%define withuuid 1
%endif

Summary: 	PostgreSQL client programs and libraries
Name:		postgresql
Version: 	9.1.1
Release: 	%mkrel 0
License:	BSD
Group:		Databases
URL:		http://www.postgresql.org/ 
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source5:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.md5
Source10:	postgres.profile
Source11:	postgresql.init
Source13:	postgresql.mdv.releasenote
Patch0:		postgresql-9.0.4_ossp-uuid-dir.patch
Requires:	perl
Provides:	postgresql-clients = %{version}-%{release}
BuildRequires:	bison flex
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	zlib-devel
%if %withuuid
BuildRequires:  ossp-uuid-devel >= 1.6.2-5
%endif
# Need to build doc
BuildRequires:  docbook-dtd42-sgml docbook-dtd44-xml
BuildRequires:	openjade docbook-utils xsltproc docbook-style-xsl
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	postgresql9.0 postgresql8.5 postgresql8.4 postgresql8.3 postgresql8.2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Provides:	postgresql-libs = %{version}-%{release}
Obsoletes:	postgresql-libs < %{current_major_version}
Obsoletes:	%{mklibname pq9.0 _5}
Obsoletes:	%{mklibname pq8.5 _5}
Obsoletes:	%{mklibname pq8.4 _5}
Obsoletes:	%{mklibname pq8.3 _5}

%description -n	%{libname}
C and C++ libraries to enable user programs to communicate with the PostgreSQL
database backend. The backend can be on another machine and accessed through
TCP/IP.

%package -n	%{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql >= %{version}-%{release}
Obsoletes:	%{mklibname ecpg9.0 _6}
Obsoletes:	%{mklibname ecpg8.5 _6}
Obsoletes:	%{mklibname ecpg8.4 _6}
Obsoletes:	%{mklibname ecpg8.3 _6}
Obsoletes:	%{mklibname ecpg 5}

%description -n	%{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C) Use
postgresql-dev to develop such programs.

%package	server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Requires(post): %{libname} >= %{version}-%{release}
Requires(preun): %{libname} >= %{version}-%{release}
# add/remove services
Requires(post): rpm-helper
Requires(preun): rpm-helper
# add/del user
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	postgresql >= %{version}-%{release}
Requires(post):	postgresql >= %{version}-%{release}
Provides:	%{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} = %{current_major_version}
Requires:	postgresql-plpgsql >= %{version}-%{release}
Obsoletes:	postgresql9.0-server postgresql8.5-server postgresql8.4-server postgresql8.3-server postgresql8.2-server

%description	server
The postgresql-server package includes the programs needed to create and run a
PostgreSQL server, which will in turn allow you to create and maintain
PostgreSQL databases.  PostgreSQL is an advanced Object-Relational database
management system (DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). You should
install postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need to
install the postgresql and postgresql-devel packages.

After installing this package, please read postgresql.mdv.releasenote.

%package	docs
Summary:	Extra documentation for PostgreSQL
Group:		Databases
Obsoletes:	postgresql9.0-docs postgresql8.5-docs postgresql8.4-docs postgresql8.3-docs postgresql8.2-docs

%description	docs
The postgresql-docs package includes the SGML source for the documentation as
well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package	contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:	postgresql-server >= %{version}-%{release}
Obsoletes:	postgresql9.0-contrib postgresql8.5-contrib postgresql8.4-contrib postgresql8.3-contrib postgresql8.2-contrib

%description	contrib
The postgresql-contrib package includes the contrib tree distributed with the
PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package	devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Provides:	postgresql-libs-devel = %{version}-%{release}
Requires:	postgresql >= %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libecpg} >= %{version}-%{release}
Obsoletes:	postgresql9.0-devel postgresql8.5-devel postgresql8.4-devel postgresql8.3-devel postgresql8.2-devel

%description	devel
The postgresql-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with a PostgreSQL
database management server and the ecpg Embedded C Postgres preprocessor. You
need to install this package if you want to develop applications which will
interact with a PostgreSQL server. If you're installing postgresql-server, you
need to install this package.

%package	pl
Summary:	Procedurals languages for PostgreSQL
Group:		Databases
Requires:	%{name}-plpython >= %{version}-%{release} 
Requires:	%{name}-plperl >= %{version}-%{release} 
Requires:	%{name}-pltcl >= %{version}-%{release} 
Requires:	%{name}-plpgsql >= %{version}-%{release} 
Obsoletes:	postgresql9.0-pl postgresql8.5-pl postgresql8.4-pl postgresql8.3-pl postgresql8.2-pl

%description	pl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pl will install the the PL/Perl, PL/Tcl, and PL/Python procedural
languages for the backend. PL/Pgsql is part of the core server package.

%package	plpython
Summary:	The PL/Python procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{current_major_version}
Obsoletes:	postgresql9.0-plpython postgresql8.5-plpython postgresql8.4-plpython postgresql8.3-plpython postgresql8.2-plpython

%description	plpython
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpython package contains the the PL/Python procedural languages for
the backend. PL/Python is part of the core server package.

%package	plperl
Summary:	The PL/Perl procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql-server >= %{version}
Requires:	perl-base >= %{perl_epoch}:%{perl_version}
Requires:	%{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{current_major_version}
Obsoletes:	postgresql9.0-plperl postgresql8.5-plperl postgresql8.4-plperl postgresql8.3-plperl postgresql8.2-plperl

%description	plperl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plperl package contains the the PL/Perl procedural languages for the
backend. PL/Perl is part of the core server package.

%package	pltcl
Summary:	The PL/Tcl procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{current_major_version}
Obsoletes:	postgresql9.0-pltcl postgresql8.5-pltcl postgresql8.4-pltcl postgresql8.3-pltcl postgresql8.2-pltcl

%description	pltcl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pltcl package contains the the PL/Tcl procedural languages for the
backend. PL/Tcl is part of the core server package.

%package	plpgsql
Summary:	The PL/PgSQL procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{current_major_version}
Obsoletes:	postgresql9.0-plpgsql postgresql8.5-plpgsql postgresql8.4-plpgsql postgresql8.3-plpgsql postgresql8.2-plpgsql

%description	plpgsql
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpgsql package contains the the PL/PgSQL procedural languages for
the backend. PL/PgSQL is part of the core server package.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1 -b .ossp-uuid_dir~

%build

%serverbuild

%configure2_5x \
    --disable-rpath \
    --with-perl \
    --with-python \
    --with-tcl --with-tclconfig=%{_libdir} \
    --with-openssl \
    --with-pam \
    --with-libxml \
    --with-libxslt \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/pgsql \
    --enable-nls \
%if %withuuid
    --with-ossp-uuid
%endif

# $(rpathdir) come from Makefile
perl -pi -e 's|^all:|LINK.shared=\$(COMPILER) -shared -Wl,-rpath,\$(rpathdir),-soname,\$(soname)\nall:|' src/pl/plperl/GNUmakefile

# nuke -Wl,--no-undefined
perl -pi -e "s|-Wl,--no-undefined||g" src/Makefile.global

%if %withuuid
# bork...
echo "#define HAVE_OSSP_UUID_H 1" >> src/include/pg_config.h
%endif

%make world

pushd src/test
make all
popd

%check
make check

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install-world install-docs

# install odbcinst.ini
mkdir -p %{buildroot}%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
#install -m755 src/Makefile.global %{buildroot}%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql

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

install -D -m755 %{SOURCE11} %{buildroot}%{_initrddir}/postgresql

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
%find_lang pg_resetxlog-%{majorversion}
cat pg_resetxlog-%{majorversion}.lang >> server.lst
%find_lang postgres-%{majorversion}
cat postgres-%{majorversion}.lang >> server.lst

# main
%find_lang pg_config-%{majorversion}
cat pg_config-%{majorversion}.lang >> main.lst
%find_lang pg_dump-%{majorversion}
cat pg_dump-%{majorversion}.lang >> main.lst
%find_lang pgscripts-%{majorversion}
cat pgscripts-%{majorversion}.lang >> main.lst
%find_lang psql-%{majorversion}
cat psql-%{majorversion}.lang >>main.lst

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
%%postgresql_major   %{current_major_version}
%%postgresql_minor   %{current_minor_version}
%%pgmodules_req Requires: %{?arch_tagged:%arch_tagged %{name}-server-ABI}%{?!arch_tagged:%{name}-server-ABI} >= %{current_major_version}
EOF

cat %{SOURCE13} > postgresql.mdv.releasenote
cat > README.urpmi <<EOF
You just installed or updated %{name} server.
You can find important information about mandriva %{name} rpms and database
management in:

%{_defaultdocdir}/%{name}-server/postgresql.mdv.releasenote

Please read it.
EOF

# postgres' .profile and .bashrc
install -D -m 700 %SOURCE10 %{buildroot}/var/lib/pgsql/.profile
(
cd %{buildroot}/var/lib/pgsql/
ln -s .profile .bashrc
)

cat > %{buildroot}%_sysconfdir/sysconfig/postgresql <<EOF
# Olivier Thauvin <nanardon@mandriva.org>

# The database location:
# You probably won't change this
# PGDATA=/var/lib/pgsql/data

# What is the based locales for postgresql
# Setting locales to C allow to use any encoding
# ISO or UTF, any other choice will restrict you
# either ISO or UTF.
LC_ALL=C

# These are additional to pass to pg_ctl when starting/restarting postgresql.
# PGOPTIONS=
EOF

# cleanup
rm -f %{buildroot}%{_libdir}/lib*.*a

%pre server
%_pre_useradd postgres /var/lib/pgsql /bin/bash

[ ! -f %pgdata/data/PG_VERSION ] && exit 0
mypgversion=`cat %pgdata/data/PG_VERSION`
[ $mypgversion = %{current_major_version} ] && exit 0

echo ""
echo "You currently have database tree for Postgresql $mypgversion"
echo "You must use postgresql${mypgversion}-server"
echo "To update you Postgresql server, dump your databases"
echo "delete /var/lib/pgsql/data/ content, upgrade the server, then"
echo "restore your databases from your backup"
echo ""

exit 1

%posttrans server

%_post_service %{name}

%preun server
%_preun_service %{name}

%postun server
%_postun_userdel postgres

%clean
rm -rf %{buildroot}

%files -f main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT README HISTORY doc/bug.template
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_basebackup
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/pg_test_fsync
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_basebackup.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%_sys_macros_dir/%{name}.macros

%files -n %{libname} -f %{libname}.lst
%defattr(-,root,root)
%{_libdir}/libpq.so.%{major}*

%files -n %{libecpg} -f %{libecpg}.lst
%defattr(-,root,root)
%{_libdir}/libecpg.so.%{major_ecpg}*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files docs
%defattr(-,root,root)
%doc %{_docdir}/%{name}-docs-%{version}

%files contrib
%defattr(-,root,root)
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/chkpass.so
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
%{_libdir}/postgresql/timetravel.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/adminpack.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/isn.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/pageinspect.so

#%{_datadir}/postgresql/contrib/
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo

%files server -f server.lst
%defattr(-,root,root)
%{_initrddir}/postgresql
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%doc README.urpmi postgresql.mdv.releasenote
%{_bindir}/initdb
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/pg_standby
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_upgrade
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%dir %{_libdir}/postgresql
%dir %{_datadir}/postgresql
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bashrc
%attr(-,postgres,postgres) /var/lib/pgsql/.profile
%attr(700,postgres,postgres) %dir %{pgdata}
%attr(-,postgres,postgres) %{pgdata}/data
%attr(700,postgres,postgres) %dir %{pgdata}/backups
%{_libdir}/postgresql/*_and_*.so
%{_libdir}/postgresql/auth_delay.so
%{_libdir}/postgresql/auto_explain.so
%{_libdir}/postgresql/btree_gin.so
%{_libdir}/postgresql/citext.so
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/dummy_seclabel.so
%{_libdir}/postgresql/euc2004_sjis2004.so
%{_libdir}/postgresql/file_fdw.so
%{_libdir}/postgresql/libpqwalreceiver.so
%{_libdir}/postgresql/passwordcheck.so
%{_libdir}/postgresql/pg_stat_statements.so
%{_libdir}/postgresql/pg_upgrade_support.so
%{_libdir}/postgresql/pgxml.so
%{_libdir}/postgresql/test_parser.so
%{_libdir}/postgresql/tsearch2.so
%{_libdir}/postgresql/unaccent.so
%if %withuuid
%{_libdir}/postgresql/uuid-ossp.so
%endif
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/postgres.description
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/timezone
%{_datadir}/postgresql/system_views.sql
%{_datadir}/postgresql/conversion_create.sql
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt
%{_datadir}/postgresql/postgres.shdescription
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

%files devel -f devel.lst
%defattr(-,root,root)
# %doc doc/TODO doc/TODO.detail
%{_includedir}/*
%{_bindir}/ecpg
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg.so
%{_libdir}/libpgtypes.so
%{_libdir}/libpq.so
%{_libdir}/postgresql/pgxs/
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*
%{_mandir}/man3/SPI_*.3*
%{_mandir}/man3/dblink*.3*

%files pl
%defattr(-,root,root)

%files plpython -f plpython.lst
%defattr(-,root,root)
%{_libdir}/postgresql/plpython*.so

%files plperl -f plperl.lst
%defattr(-,root,root)
%{_libdir}/postgresql/plperl.so

%files pltcl -f pltcl.lst
%defattr(-,root,root)
%{_libdir}/postgresql/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/postgresql/unknown.pltcl

%files plpgsql -f plpgsql.lst
%defattr(-,root,root)
%{_libdir}/postgresql/plpgsql.so
