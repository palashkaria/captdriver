check_PROGRAMS = captdefilter test-hiscoa

hiscoa_decompress = \
	hiscoa-decompress.c \
	hiscoa-decompress.h

captdefilter_SOURCES = captdefilter.c \
	$(hiscoa_decompress)

test_hiscoa_SOURCES = test-hiscoa.c \
	../src/hiscoa-compress.c \
	$(hiscoa_decompress)

AM_CFLAGS = -std=c99 -Wall -Wextra -pedantic -I../src

EXTRA_DIST = test-backend-drain.py
if PERSISTENT_USB
TESTS = test-backend-drain.py
AM_TESTS_ENVIRONMENT = CAPT_BACKEND='$(abs_top_builddir)/persistent/capt'; export CAPT_BACKEND;
endif
