# System modifications
Which persistent modifications have we done to the system? It is a good idea to keep track of file modifications, BIOS changes etc. in case a problem arises.

## Grub
Edit /boot/grub/grub.conf and add the intel_idle.max_cstate=0 parameter to the kernel
line.

## BIOS

### **Under system settings/Operating Modes**

choose Custom instead of Maximum Perfomance under Choose operating mode
Should possibly also enable P-state and C-state in the same window.
Disable Intel virtualization technology

### **Under system settings/processors**
Enable p-states and c-states
Disable d-states? D0 is ASPM according to https://lenovopress.com/lp0632.pdf
Disable HW prefetcher, Adjacent Cache prefetch and DCU streamer prefetcher
Enable DCA(Enable as standard)


### **Under system settings/ Devices and I/O Ports**
Disable Intel VT-d
"Disable IOMMU in system BIOS setup by setting “Intel VT-d” to Disabled.  The typical menu entry for this option is:
Advanced -> Chipset Configuration -> Intel VT-d
Disable IOMMU in Linux by adding “intel_iommu=off” to the Linux kernel bootup parameter."


# Notes
