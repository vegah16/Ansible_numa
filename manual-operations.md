# Manual operations
These operations are deemed too advanced for automation, and should be done manually.

## Isolate CPU cores from general system processes
Add a boot kernel parameter in order to isolate the CPUs from the rest of the system. They can then be used solely for Suricata without interruptions.


Edit file: `/etc/default/grub`

Change the line:

`GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"`

to:

`GRUB_CMDLINE_LINUX_DEFAULT="quiet splash isolcpus=1"`

This will isolate CPU 1. In order to isolate CPUs 6-12, add `isolcpus=6-12`

Finally, update grub by running:

`$ update-grub`