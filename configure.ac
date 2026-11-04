AC_PREREQ([2.69])
AC_INIT([captdriver], [0.1.4.1])

AC_CONFIG_SRCDIR([src/std.h])

AM_INIT_AUTOMAKE([1.9 no-dist-gzip dist-xz tar-ustar subdir-objects])
AM_SILENT_RULES([yes])

AC_LANG([C])
AC_PROG_CC

AC_PATH_PROG([CUPS_CONFIG], [cups-config])
if test -z "${CUPS_CONFIG}"; then
    AC_MSG_FAILURE([CUPS library not found.])
fi
CUPS_CFLAGS="`${CUPS_CONFIG} --cflags`"
CUPS_LIBS="`${CUPS_CONFIG} --image --libs`"
AC_SUBST(CUPS_CFLAGS)
AC_SUBST(CUPS_LIBS)

AC_ARG_WITH([cups-serverbin],
    [AS_HELP_STRING([--with-cups-serverbin=DIR], [CUPS filter/backend directory])],
    [CUPS_SERVERBIN="$withval"], [CUPS_SERVERBIN="`$CUPS_CONFIG --serverbin`"])
AC_SUBST([CUPS_SERVERBIN])
AC_ARG_ENABLE([persistent-usb],
    [AS_HELP_STRING([--enable-persistent-usb], [build Linux LBP2900 persistent USB daemon/backend])],
    [], [enable_persistent_usb=no])
AS_CASE([$enable_persistent_usb], [yes|no], [],
    [AC_MSG_ERROR([--enable-persistent-usb must be yes or no])])
AM_CONDITIONAL([PERSISTENT_USB], [test "x$enable_persistent_usb" = xyes])
AS_IF([test "x$enable_persistent_usb" = xyes], [
    PKG_CHECK_MODULES([LIBUSB], [libusb-1.0])
])
AC_ARG_WITH([systemdunitdir],
    [AS_HELP_STRING([--with-systemdunitdir=DIR], [systemd service unit directory])],
    [SYSTEMD_UNITDIR="$withval"], [SYSTEMD_UNITDIR='${prefix}/lib/systemd/system'])
AC_SUBST([SYSTEMD_UNITDIR])

AC_CONFIG_FILES([Makefile
                 persistent/Makefile
                 src/Makefile
                 tests/Makefile
                ])
AC_OUTPUT
