# Source provenance

## Driver baseline

Repository: https://github.com/ValdikSS/captdriver
Branch: `val`
Commit: `892f320c019974a5b737e000fcc2c8582264a131`

Existing source history, AUTHORS and GPL-3.0 COPYING are retained.

## Imported persistent-session and protocol work

Repository: https://github.com/brucenguyen1102/Canon-LBP2900-CAPT-Toolkit
Commit: `4b8c50cfd0bc67423fa68409d9f1141df857fae5`
Directory: `captd-persistent-daemon/`

Imported driver replacements: `capt-command.c`, `capt-status.c`,
`capt-status.h`, `generic-ops.c`, `printer.h`, `prn_lbp2900.c`.
Imported new transport components: `captd.c`, `capt-backend.c`.
Original source comments/notices are retained as supplied. These additions
are attributed to the CAPT Toolkit and its author Bruce Nguyen, rather
than presented as original work of this fork. The toolkit did not include
a separate license file at the imported revision.

## Local changes

- Root-only daemon socket permissions.
- Correct output-drain ordering, nonblocking print reads and 4 KB frame limit.
- Hardware-free regression tests against the actual backend.
- Build/install integration, systemd packaging and optional Proxmox examples.

The protocol/filter sources and transport behavior were copied from the
working installation before packaging. Build paths, test paths and the
example container ID were generalized for publication. No printer jobs,
private configuration, credentials or binaries were imported.
