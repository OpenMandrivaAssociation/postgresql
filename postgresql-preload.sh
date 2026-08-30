#!/bin/sh
# Merge packaged/admin preload modules with the cluster's
# shared_preload_libraries. Used by postgresql.service and the
# major-version upgrade path in postgresql_initdb.sh.
#
# Usage:
#   postgresql-preload.sh guc [PGDATA]   print merged module list
#   postgresql-preload.sh exec [args]    exec postgres with the list
#
# Package drop-ins: @SYS_PRELOAD@/<module>
# Admin drop-ins:   @ETC_PRELOAD@/<module>
# Basename is the module name (optional .so suffix is stripped).
# A module whose shared object is not in @PKGLIBDIR@ is skipped.

PKGLIBDIR="@PKGLIBDIR@"
SYS_PRELOAD="@SYS_PRELOAD@"
ETC_PRELOAD="@ETC_PRELOAD@"

modules=

module_exists() {
	name=$1
	case "$name" in
	/*)
		[ -e "$name" ] || [ -e "$name.so" ]
		;;
	*)
		[ -e "$PKGLIBDIR/$name.so" ]
		;;
	esac
}

has_module() {
	case ",$modules," in
	*",$1,"*)
		return 0
		;;
	*)
		return 1
		;;
	esac
}

add_module() {
	name=$1
	name=${name%.so}
	name=$(printf '%s' "$name" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
	[ -n "$name" ] || return 0
	if has_module "$name"; then
		return 0
	fi
	if ! module_exists "$name"; then
		echo "postgresql-preload: skipping missing module '$name'" >&2
		return 0
	fi
	if [ -n "$modules" ]; then
		modules="$modules,$name"
	else
		modules="$name"
	fi
}

scan_dir() {
	dir=$1
	[ -d "$dir" ] || return 0
	for path in "$dir"/*; do
		[ -f "$path" ] || continue
		base=${path##*/}
		case "$base" in
		.*|*~|*.rpmnew|*.rpmsave|*.rpmorig|*.swp|README|README.*)
			continue
			;;
		esac
		add_module "$base"
	done
}

compute_guc() {
	pgdata=$1
	modules=
	if [ -n "$pgdata" ] && [ -f "$pgdata/PG_VERSION" ]; then
		current=$(/usr/bin/postgres -D "$pgdata" -C shared_preload_libraries 2>/dev/null || true)
		if [ -n "$current" ]; then
			oldifs=$IFS
			IFS=,
			# shellcheck disable=SC2086
			set -- $current
			IFS=$oldifs
			for item in "$@"; do
				add_module "$item"
			done
		fi
	fi
	scan_dir "$SYS_PRELOAD"
	scan_dir "$ETC_PRELOAD"
}

cmd=${1:-guc}
shift

case "$cmd" in
guc)
	pgdata=${1:-${PGDATA:-/srv/pgsql/data}}
	compute_guc "$pgdata"
	printf '%s\n' "$modules"
	;;
exec)
	pgdata=${PGDATA:-/srv/pgsql/data}
	pgport=${PGPORT:-5432}
	compute_guc "$pgdata"
	if [ -n "$modules" ]; then
		exec /usr/bin/postgres -D "$pgdata" -p "$pgport" \
			-c "shared_preload_libraries=$modules" "$@"
	fi
	exec /usr/bin/postgres -D "$pgdata" -p "$pgport" "$@"
	;;
*)
	echo "usage: $0 guc [PGDATA] | exec [postgres-args...]" >&2
	exit 2
	;;
esac
