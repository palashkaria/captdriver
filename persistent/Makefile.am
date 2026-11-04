EXTRA_DIST = captd.c capt-backend.c ../packaging/systemd/captd.service.in

if PERSISTENT_USB
sbin_PROGRAMS = captd
cupsbackenddir = $(CUPS_SERVERBIN)/backend
cupsbackend_PROGRAMS = capt
captd_SOURCES = captd.c
captd_CPPFLAGS = -D_DEFAULT_SOURCE $(LIBUSB_CFLAGS)
captd_LDADD = $(LIBUSB_LIBS) -lpthread
capt_SOURCES = capt-backend.c
capt_CPPFLAGS = -D_DEFAULT_SOURCE $(CUPS_CFLAGS)
capt_LDADD = $(CUPS_LIBS)
AM_CFLAGS = -std=c99 -Wall -Wextra -fstack-protector-strong

systemdunitdir = $(SYSTEMD_UNITDIR)
systemdunit_DATA = captd.service
CLEANFILES = captd.service
captd.service: $(srcdir)/../packaging/systemd/captd.service.in Makefile
	$(AM_V_GEN)sed 's|@CAPTD_EXECUTABLE@|$(sbindir)/captd|g' $< > $@

install-data-hook:
	chmod 0700 "$(DESTDIR)$(cupsbackenddir)/capt"
endif
