#!/bin/sh
# based on the init script for starting up the PostgreSQL server

PGDATA=$1

RETVAL=0

# Check for the PGDATA structure
if [ ! -f ${PGDATA}/PG_VERSION ]; then
	if [ ! -d ${PGDATA} ]; then
		mkdir -p ${PGDATA}
		chown postgres:postgres ${PGDATA}
		chmod go-rwx ${PGDATA}
	fi
	# Initialize the database
	/usr/bin/initdb --pgdata=${PGDATA} &>> /var/log/postgres/postgresql && test -f ${PGDATA}/PG_VERSION
	RETVAL=$?

	# Check if we're updating
	MAJORVERSION="$(postgres --version |cut -d' ' -f3 |cut -d. -f1)"
	UPDIR="$(ls -1d @PGDIR@/update-from-*-to-${MAJORVERSION} |head -n1 2>/dev/null)"
	if [ -d "$UPDIR" ]; then
		OLDMAJOR=$(echo $UPDIR |sed -e 's,.*update-from-,,;s,-.*,,')
		echo "Resuming update from ${OLDMAJOR} to ${MAJORVERSION}"
                cp -af @PGDIR@/data-from-${OLDMAJOR}/*.{conf,opts} "${PGDATA}"
                pg_ctl start -D ${PGDATA} -s -o "-p 5432" -w -t 300
                psql -f ${UPDIR}/db.dump postgres &>${UPDIR}/restore.log
                vacuumdb -a -z &>${UPDIR}/vacuumdb.log
                pg_ctl stop -D "${PGDATA}"
		cat >&2 <<EOF
================================================================
PostgreSQL has been updated from ${OLDMAJOR} to ${MAJORVERSION}
All databases have been migrated automatically.

In case there are any problems with the update/migration,
you can find a backup of the databases for PostgreSQL ${OLDMAJOR}
in @PGDIR@/data-from-${OLDMAJOR}, and you can find the
database dump used for migration in
${UPDIR}

If you're satisfied that everything is working after the update,
you may want to save space by removing those backups:
rm -rf @PGDIR@/data-from-* @PGDIR@/update-from-*

If, for some reason, you need to go back to the old version,
remove the current PostgreSQL packages, and run:
cd @PGDIR@
rm -rf data
mv data-from-${OLDMAJOR} data
And reinstall the old PostgreSQL version.
================================================================
EOF
	fi
fi
exit $RETVAL
