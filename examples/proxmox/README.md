# Optional Proxmox reconnect helper

These examples belong on the Proxmox host, not inside the print container.
They are not installed automatically. The container should be dedicated to
printing: reconnect recovery restarts that container and may interrupt an
active print job.

The helper matches only Canon USB ID `04a9:2676`. It uses Proxmox `dev0`
with uid 0, gid 7 and mode 0660 inside an unprivileged container. `dev0`
must be reserved for this printer. No whole USB bus mount or wildcard
device access is required. Multiple matching printers are not supported.

Choose your container ID and create `/etc/default/canon-printer-sync`:

```sh
CT_ID=YOUR_PRINT_CONTAINER_ID
```

Replace the placeholder with a numeric container ID. Then copy
`canon-printer-sync` to `/usr/local/sbin/` (mode 0750), and the `.service`
and `.timer` files to `/etc/systemd/system/`. Enable them on the host:

```sh
systemctl daemon-reload
systemctl enable --now canon-printer-sync.service canon-printer-sync.timer
```

The service runs after `pve-cluster` and before guest autostart. Its timer
checks every 15 seconds. A changed USB path/inode triggers these steps:

1. Stop the print container if it was running.
2. Set its single-device `dev0` mapping, or remove it if the printer is absent.
3. Restart the container only if it was previously running.

Stopping before `pct set` matters: a live replacement can fail when the
old USB node no longer exists. Allow roughly 30 seconds after reconnects.
The daemon inside the container is enabled independently with `captd.service`.

Keep the `canon-printer-sync` service name/lock/state paths unique if
adapting this example for a different device or container.
