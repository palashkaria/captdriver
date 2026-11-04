SUBDIRS = src persistent tests

dist_doc_DATA = SPECS INSTALL.git README.md docs/CHANGES.md docs/PROVENANCE.md
EXTRA_DIST = src/canon-lbp.drv ppd examples/proxmox/README.md \
    examples/proxmox/canon-printer-sync \
    examples/proxmox/canon-printer-sync.service \
    examples/proxmox/canon-printer-sync.timer
nodist_data_DATA = Makefile.in

ppd: src/canon-lbp.drv
	LC_ALL=C LC_NUMERIC=C ppdc src/canon-lbp.drv -d ./ppd

clean-ppd:
	-rm -rf ppd
