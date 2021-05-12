# TODOs

# Local bypass (DONE)
source: SEPTun
Should be tested

# XDP & BPF (FAIL)
source: SEPTun 2
Consider testing this after everything else. Apply XDP to best setup.

# Test NIC ring descriptor size (DONE)
Test other values for `ethtool -G ens2f0 rx 1024` like 512.
Lowering it could make the DDIO work better and lower L3 cache misses. Smaller buffers means
interrupts should run more frequently. So, try also to lower last number in
`ethtool -C {{monitor_if}} adaptive-rx off adaptive-tx off rx-usecs 125`. Maybe 60.

# Test NIC balancing (NO)
sdfn vs sd
