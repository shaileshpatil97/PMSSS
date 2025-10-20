try:
	import pymysql  # type: ignore

	pymysql.install_as_MySQLdb()
except Exception:
	# PyMySQL may not be installed in SQLite-only setups; ignore.
	pass

