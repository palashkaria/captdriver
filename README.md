# captdriver: Canon CAPT printing with a persistent USB session

This fork starts from [ValdikSS/captdriver](https://github.com/ValdikSS/captdriver/tree/val),
branch `val`, commit `892f320c019974a5b737e000fcc2c8582264a131`.
It packages the LBP2900 protocol and persistent-session fixes from
[Canon-LBP2900-CAPT-Toolkit](https://github.com/brucenguyen1102/Canon-LBP2900-CAPT-Toolkit)
and adds a tested fix for premature output-drain acknowledgements.
See [the changes](docs/CHANGES.md) and [source provenance](docs/PROVENANCE.md).

The persistent path has been exercised with a USB Canon LBP2900 on x86-64
Debian 13, shared by CUPS to a Mac over IPP. Other printer models have not
been validated with these additions. The daemon explicitly selects USB
vendor/product `04a9:2676` and assumes a little-endian host.

## Build on Debian or Ubuntu

```sh
sudo apt-get install build-essential autoconf automake pkg-config   libcups2-dev libcupsimage2-dev libusb-1.0-0-dev cups cups-filters   cups-ppdc avahi-daemon python3
autoreconf -fi
./configure --enable-persistent-usb
make
make ppd
make check
```

`make check` exercises the actual backend against a fake USB daemon. It
checks that output is acknowledged only after USB completion and that
frames never exceed 4096 bytes. It prints no pages and needs no root access.

Without `--enable-persistent-usb`, only the conventional raster filter is
built. The conventional `usb://` path still needs a CUPS USB backend with
the [upstream race fix](https://github.com/OpenPrinting/cups/issues/1461),
available in CUPS 2.4.17+. The `capt:` path below bypasses that backend.

## Install the persistent LBP2900 path

Pause the printer queue and wait for any active job to finish before
replacing an existing installation. Back up its filter and queue settings.
The following commands configure a new queue named `Canon2900`:

```sh
sudo make install
sudo systemctl daemon-reload
sudo systemctl enable --now captd.service
sudo lpadmin -p Canon2900 -E   -v capt:/run/captd/lbp2900.sock   -P ppd/CanonLBP-2900-3000.ppd   -D 'Canon LBP2900 (Network)'   -o PageSize=A4 -o printer-is-shared=true   -o printer-error-policy=stop-printer
sudo cupsctl --share-printers
sudo systemctl enable --now avahi-daemon
```

The filter/backend install beneath `cups-config --serverbin`; `captd`
installs under the configured prefix (default `/usr/local/sbin`).
The systemd unit uses that same prefix. `DESTDIR` is supported for staged
installs. `--with-cups-serverbin=DIR` and `--with-systemdunitdir=DIR`
allow packagers to override the destinations.

`captd` holds one USB connection open across jobs. The CUPS `capt` backend
communicates with it through `/run/captd/lbp2900.sock`. The socket is mode
0600 in a mode-0700 directory, and the backend is installed mode 0700 so
CUPS runs it as root. No TCP listener is added by the daemon.

Clients can add `ipp://PRINT_SERVER:631/printers/Canon2900`. A Mac can use
IPP Everywhere; it does not need the Canon direct-USB patch for this queue.
CUPS sharing permits the local network by default. Discovery across
subnets or VPNs needs separate network configuration.

## Recovery and deployment notes

- Do not point a second queue at the same USB printer: `captd` owns its USB interface.
- An already-wedged engine may need one physical power cycle before retrying
  the stopped job. Fixing the driver does not reset the printer's firmware.
- Paper jams, an open cover or a missing cartridge may still require clearing
  the physical problem and reprinting; transparent recovery is not guaranteed.
- Inspect `journalctl -u captd` and `/var/log/cups/error_log` for failures.
- After correcting an error, enable the queue and explicitly restart a stopped
  job if necessary: `sudo cupsenable Canon2900`, then `lp -i Canon2900-JOB_ID -H restart`.
- [Proxmox container examples](examples/proxmox/README.md) pass through only
  this Canon device and refresh its mapping after a power cycle. They are
  optional and are not installed by `make install`.

## Credits and license

The original driver is by Alexey Galakhov and subsequent contributors,
including Mounaiban and ValdikSS. ValdikSS added page streaming, paper
geometry, performance and protocol improvements. Bruce Nguyen's CAPT
Toolkit supplied the persistent daemon/backend and additional protocol
recovery work. This fork adds the output-drain fix, tests and packaging.
Original notices are retained; see [AUTHORS](AUTHORS), [COPYING](COPYING)
and [provenance](docs/PROVENANCE.md).

This is unofficial software and is not endorsed by Canon.
