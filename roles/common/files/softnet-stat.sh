softnet_stat_output() {
    TYP=$1
    IDX=$2

    METRIC="softnet_stat"

    VAL=$(cat /proc/net/softnet_stat | awk -v IDX="$IDX" '{sum+=strtonum("0x"$IDX);} END{print sum;}')
    TAGS="{\"type\":\"$TYP\"}";

    echo $METRIC$TAGS $VAL;
}

# Format of /proc/net/softnet_stat:
#
# column 1  : received frames
# column 2  : dropped
# column 3  : time_squeeze
# column 4-8: all zeros
# column 9  : cpu_collision
# column 10 : received_rps
# column 11 : flow_limit_count
#
# http://arthurchiao.art/blog/tuning-stack-rx-zh/
softnet_stat_output "dropped" 2
softnet_stat_output "time_squeeze" 3
softnet_stat_output "cpu_collision" 9
softnet_stat_output "received_rps" 10
softnet_stat_output "flow_limit_count" 11