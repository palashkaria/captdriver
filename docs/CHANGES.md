# Changes from ValdikSS `val`

Baseline: `892f320c019974a5b737e000fcc2c8582264a131`.

## Protocol and recovery changes imported from the CAPT Toolkit

- Repeated `SetJobInfo2(CONT)` heartbeats during physical printing.
- Two unconditional extended-status requests before reserving the LBP2900.
- Corrected page payload flags, toner-density bytes and Linux job-end value.
- Read complete replies even when the back channel returns partial data.
- Bounded reply-stream resynchronization for stale bytes left by a prior job.
- Bounded status and buffer-drain waits, backed-off polling, richer diagnostics.

These change six driver files: `capt-command.c`, `capt-status.c`,
`capt-status.h`, `generic-ops.c`, `printer.h`, and `prn_lbp2900.c`.
The toolkit's `capt-command.h` matched the baseline and is unchanged.

## Persistent USB transport

- `persistent/captd.c`: one claimed USB interface across print jobs, framing,
  USB-completion acknowledgements, and stale-reply drains between clients.
- `persistent/capt-backend.c`: CUPS side/back-channel bridge to the daemon.
- The daemon and all protocol changes are intended to be used together.
  Persistence alone was not sufficient in the toolkit's investigation.
- Local socket permissions tightened from 0666 to 0600; runtime directory 0700.
- A restricted systemd unit starts the daemon automatically and restarts it on failure.

## Local output-drain correction

The imported backend could process a CUPS `DRAIN_OUTPUT` request before
reading data already waiting in the print pipe. With zero outstanding
frames, it acknowledged completion before forwarding that data to USB.

The corrected handler makes print input nonblocking, forwards all pending
input, and waits for the daemon to acknowledge every forwarded frame
before answering CUPS. Reads and frames are limited to 4096 bytes;
`EAGAIN`/`EWOULDBLOCK` are handled without failing the job.

`tests/test-backend-drain.py` starts the real backend with both channels
ready, deliberately withholds the mock USB acknowledgement, and asserts
that CUPS receives no premature acknowledgement. A second case checks a
payload spanning two frames. No printer hardware is used.

## Packaging and deployment

- Optional `--enable-persistent-usb` integrates daemon/backend with Automake.
- `make install` installs the raster filter directly into CUPS's filter directory.
- Configurable CUPS/systemd paths and `DESTDIR` support.
- CI builds conventional and persistent configurations, tests and staged installs.
- Optional parameterized Proxmox reconnect helper: stop the dedicated container
  before replacing a disappeared device node, then restart it. No wildcard
  USB permission or whole-bus bind mount is used.

## Observed validation

On one Debian 13/x86-64 server with an LBP2900, the initial setup failed on
its fifth job with `ReserveUnit 0x8c`. The persistent transport/protocol
changes cleared that failure, but exposed intermittent `no reply` errors.
After the local output-drain correction, the two remaining jobs and two
subsequent hotel PDFs completed without another error. The same daemon
held its USB session throughout that run. The drain-order regression also
passed ten consecutive hardware-free runs.

This is limited hardware evidence, not a claim that every error condition
or every supported upstream printer has been tested. No print documents,
personal details or server addresses are included in this repository.
