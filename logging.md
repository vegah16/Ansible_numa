# Logging

## stats.log
These counters are of interest, and can be plotted using suri-stats.

### capture.kernel_packets

### capture.kernel_drops

### tcp.reassembly_gap
An indicator of kernel drops, as it accounts missing data packets in TCP streams.

## mpstat for CPU utilization log

### %usr
Show the percentage of CPU utilization that occurred while executing at the user level (application).

### %nice
Show the percentage of CPU utilization that occurred while executing at the user level with nice priority.

### %sys
Show the percentage of CPU utilization that occurred while executing at the system level (kernel). Note that this does not include time spent servicing hardware and software interrupts.
### %iowait
Show the percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request.

### %irq
Show the percentage of time spent by the CPU or CPUs to service hardware interrupts.

### %soft
Show the percentage of time spent by the CPU or CPUs to service software interrupts.

### %steal
Show the percentage of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor.

### %guest
Show the percentage of time spent by the CPU or CPUs to run a virtual processor.

### %gnice
Show the percentage of time spent by the CPU or CPUs to run a niced guest.

### %idle
Show the percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request.


## Start mpstat for CPU interrupts log
Values taken from /proc/softirqs. Hard to find info.

### intr/s
Show the total number of interrupts received per second by the CPU or CPUs.

### HI/s
Handles high priority tasklets

### TIMER/s
Tasklets related to timer interrupts

### NET_TX
Transmits packets to network cards

### NET_RX
Receives packets from network cards

### BLOCK/s


### IRQ_POLL


### TASKLETS/s
Handles regular tasklets

### SCHED/s


### HRTIMER/s


### RCU/s



## Start perf for cache miss stats.
### LCC-loads
Last level cache (LLC) read accesses by a CPU core

### LCC-loads-misses
Last level cache (LLC) read misses by a CPU core

### LCC-stores
Last level cache (LLC) writes by a CPU core

### LCC-prefetches
Last level cache (LLC) prefetch accesses by a CPU core


## Start pidstat for monitoring Suricata tasks
### cswch/s
Total number of voluntary context switches the task made per second. A voluntary context switch occurs when a task blocks because it requires a resource that is unavailable.

### nvcswch/s
Total number of non voluntary context switches the task made per second. A involuntary context switch takes place when a task executes for the duration of its time slice and then is forced to relinquish the processor.


## Start softnet-stat.pl for monitoring packet drops at the softirq layer.
SEPTun 1

### total/sec
Total number of frames processed

### dropped/sec
Number of frames dropped

### squeezed/sec
Number of times softirq had more frames to process but ran out of
pre-configured time or the number of frames was too large. If this keeps
growing, than increasing the netdev_budget might help.

### collision/sec
A number of times collision occurred when a transmit path tried to
obtain a device lock. Unimportant here.

### rx_rps/sec
Number of inter-CPU interrupts, for kicking off processing of
a backlog queue on a remote CPU, used only by RPS and RFS and
not enabled by default

### flow_limit/sec
Used only by RFS, not here
