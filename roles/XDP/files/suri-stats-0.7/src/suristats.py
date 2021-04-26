#!/usr/bin/env python
# Copyright (C) 2012,2013 Eric Leblond <eric@regit.org>
#
# You can copy, redistribute or modify this Program under the terms of
# the GNU General Public License version 3 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# version 3 along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import re
import numpy
import os
import sys
HAVE_SQLITE3 = True
try:
    import sqlite3
except:
    HAVE_SQLITE3 = False
    pass
from time import sleep
from copy import copy

class Counter:
    def __init__(self, name, threadname):
        self.name = name
        self.threadname = threadname
        self.values = {}
    def add_value(self, time, value):
        self.values[time] = value
    def get_value(self, time):
        try:
            return self.values[time]
        except:
            return None
    def get_values(self):
        return self.values
    def get_times(self):
        return sorted(self.values.keys())
    def merge(self, cnt):
        for time in cnt.get_times():
            if self.values.has_key(time):
                self.values[time] += int(cnt.get_value(time))
            else:
                self.values[time] = int(cnt.get_value(time))
    def derivative(self):
        deriv = Counter(self.name + "/s", self.threadname)
        prevv = 0
        i = 0
        for time in sorted(self.values.keys()):
            if i == 0:
                prev = time
            else:
                deriv.add_value(time, (float(self.get_value(time) - self.get_value(prev)))/float(time - prev))
            i += 1
        return deriv
    def normalize(self):
        norm = Counter(self.name + " [%]", self.threadname)
        maxim = max(self.values.values())
        for time in sorted(self.values.keys()):
            norm.add_value(time, float(self.get_value(time))/float(maxim))
        return norm

class Stats:
    FAIL_COUNTERS = ['capture.kernel_drops',
                     'defrag.max_frag_hits',
                     'flow.emerg_mode_entered',
                     'tcp.segment_memcap_drop',
                     'tcp.ssn_memcap_drop',
                     'tcp.stream_depth_reached',
                     ]
    """
    Class storing the statistics of a complete run
    """
    def __init__(self, runname):
        self.name = runname
        self.counters = {}
        self.runs = []
    def load_file(self, filename):
        """
        Load a stats.log file and populate the current object.

        Keywords argument:
        filename -- a suricata stats.log file
        """
        logtime = ""
        reg_date = re.compile("uptime: (\d+)d, (\d+)h (\d+)m (\d+)s")
        prevtime = 0
        runname = self.name
        
        i = 0
        ST = self
        for line in open(filename, 'r'):
            if "----" in line:
                continue
            elif "Date:" in line:
                time_split = reg_date.search(line)
                logtime = 86400 * int(time_split.group(1)) + 3600 * int(time_split.group(2)) + 60 * int(time_split.group(3)) + int(time_split.group(4))
                if int(logtime) < prevtime:
                    self.runs.append(ST)
                    i = i + 1
                    ST = Stats(runname + '-' + str(i))
                prevtime = int(logtime)
                continue
            elif "Counter" in line:
                continue
            else: #try to parse
                try:
                    (name, threadname, value) = line.split("|")
                    ST.add_value(name.strip(), threadname.strip(), logtime, int(value.strip()))
                except:
                    sys.stderr.write("Invalid line at l.%d: '%s'\n" % (i, line))
                    pass
        self.runs.append(ST)

    def add_json_event(self, logtime, ST, event, prefix, threadname="total"):
        if event.has_key('threads'):
            for attribute, value in event['threads'].iteritems():
                self.add_json_event(logtime, ST, value, [], threadname = attribute)
        else:
            for attribute, value in event.iteritems():
                if isinstance(value, ( int, long )):
                    counter = copy(prefix)
                    counter.append(attribute)
                    ST.add_value(".".join(counter), threadname, logtime, value)
                elif isinstance(value, unicode):
                    continue
                else:
                    nprefix = copy(prefix)
                    nprefix.append(attribute)
                    self.add_json_event(logtime, ST, value, nprefix, threadname = threadname)

    def load_json_file(self, filename):
        """
        Load a eve.json file and populate the current object.

        Keywords argument:
        filename -- a suricata eve.json file
        """

        import json
        runname = self.name
        prevtime = 0
        
        i = 0
        ST = self
        for line in open(filename, 'r'):
            if not '"stats"' in line:
                continue
            try:
                event = json.loads(line)
            except:
                sys.stderr.write("Invalid line at l.%d: '%s'\n" % (i, line))
                continue
            if event.has_key('event_type') and event['event_type'] == 'stats':
                logtime = event['stats']['uptime']
                if logtime < prevtime:
                    self.runs.append(ST)
                    i = i + 1
                    ST = Stats(runname + '-' + str(i))
                prevtime = logtime
                prefix = []
                self.add_json_event(logtime, ST, event['stats'], prefix)
        self.runs.append(ST)


    def add_value(self, name, threadname, time, value):
        try:
            self.counters[name][threadname].add_value(time, value)
        #TODO exception : no key only
        except KeyError:
            if not self.counters.has_key(name):
                self.counters[name] = {}
            if not self.counters[name].has_key(threadname):
                self.counters[name][threadname] = Counter(name, threadname)
            self.counters[name][threadname].add_value(time, value)
    # TODO add way to get global counter
    def get_value(self, time, name, threadname):
        try:
            return self.counters[name][threadname].get_value(time)
        except:
            return None
    def get_values(self, name, threadname = "all"):
        return self.get_counter(name, threadname).get_values()
    def get_counter(self, name, threadname = "all"):
        if threadname == "all":
            res = Counter(name, "all")
            for key in self.counters[name].keys():
                res.merge(self.counters[name][key]) 
            return res
        else:
            return self.counters[name][threadname]

    def list_counters(self):
        return sorted(self.counters.keys())
    def list_threads(self, counter="decoder.pkts"):
        return sorted(self.counters[counter].keys())
        #try:
        #    return self.counters[name][threadname].get_values()
        #except:
        #    return None
    def list_failures(self, threadname='all', skip_init=False):
        failed = {}
        # Get counters valid for current suricata
        fail_counters = [val for val in self.list_counters() if val in self.FAIL_COUNTERS]
        for counter in fail_counters:
            i = 0
            res = self.get_counter(counter, threadname=threadname)
            start_val = 0
            for k in res.get_times():
                if i == 0:
                    i = 1
                    if skip_init:
                        start_val = res.get_values()[k]
                        continue
                    else:
                        start_val = 0
                if res.get_values()[k] > start_val:
                    failed[counter] = [k, res.get_values()[k]]
                    break
        return failed

    def plot(self, name, threadname="all", merge=True, scale=1, speed=False, normalize=False, filename=None):
        from pylab import plot, legend, savefig
        if threadname == "all" and merge != True:
            for thname in self.counters[name].keys():
                res = self.get_counter(name, thname)
                if speed == True:
                    res = res.derivative()
                    label = "%s/%s (%s)" % (thname, self.name)
                elif normalize == True:
                    res = res.normalize()
                    label = "%s [%] (%s)" % (name, self.name)
                else:
                    label = "%s (%s)" % (thname, self.name)
                res = res.get_values()
                plot(res.keys(),  numpy.multiply(scale, res.values()), '+', label=label)
        else:        
            res = self.get_counter(name, threadname)
            if speed == True:
                res = res.derivative()
                label = "%s/%s" % (name, self.name)
            elif normalize == True:
                res = res.normalize()
                label = "%s [%] (%s)" % (name, self.name)
            else:
                label = "%s (%s)" % (name, self.name)
            res = res.get_values()
            plot(res.keys(), numpy.multiply(scale, res.values()), '+', label=label)
        try:
            legend(fontsize=10)
        except TypeError:
            legend()
        if filename:
            savefig(filename)

    def output_to_file(self, filename, format='csv', mode='short'):
        OUT=open(filename,'w')
        if mode == 'short':
            OUT.write("counter,thread,time,value\n")
            for counter in self.list_counters():
                for thread in self.list_threads(counter=counter):
                    table=self.get_values(counter, threadname=thread)
                    for key in table.keys():
                        OUT.write(counter + "," + thread + "," + str(key) + "," + str(table[key])+"\n")
        elif mode == 'time':
            ordered_counters = sorted(self.list_counters())
            nb_counters = len(ordered_counters)
            OUT.write("time,thread," + ",".join(ordered_counters)+"\n")
            for key in sorted(self.get_values('decoder.pkts')):
                t_values = {}
                # get all counter for a thread
                for counter in self.list_counters():
                    for thread in self.list_threads(counter=counter):
                        if not t_values.has_key(thread):
                            t_values[thread] = {}
                        t_values[thread][counter] = self.get_values(counter, threadname=thread)[key]
                for thread in t_values.keys():
                    OUT.write(str(key) + "," + thread + ",")
                    i = 0
                    for counter in ordered_counters:
                        if t_values[thread].has_key(counter):
                            OUT.write(str(t_values[thread][counter]))
                        i += 1
                        if i < nb_counters:
                            OUT.write(",")
                    OUT.write("\n")
        OUT.close()
    def op(self, counters_list=None, speed=False, func=min):
        if counters_list == None:
            counters_list = self.list_counters()
        res = {}
        for counter in counters_list:
            data = self.get_counter(counter)
            if speed:
                data = data.derivative()
            res[counter] = func(data.get_values().values())
        return res
    def min(self, counters_list=None, speed=False):
        return self.op(counters_list=counters_list, speed=speed, func=min)
    def max(self, counters_list=None, speed=False):
        return self.op(counters_list=counters_list, speed=speed, func=max)
    def mean(self, counters_list=None, speed=False):
        return self.op(counters_list=counters_list, speed=speed, func=numpy.mean)
    def std(self, counters_list=None, speed=False):
        return self.op(counters_list=counters_list, speed=speed, func=numpy.std)

class DBStats:
    def __init__(self, db_file):
        if not HAVE_SQLITE3:
            raise Exception('sqlite3 module is not available')
        self.db_file = db_file
        #self.counters = {}
    def init_db(self):
        if os.path.isfile(self.db_file):
            sys.stderr.write("Will not overwrite existing file\n")
            sys.exit(1)
        conn = sqlite3.connect(self.db_file)
        conn.execute('''CREATE TABLE counters
                 (timestamp float, run_id text, host_id text, version text, counter text, min real, mean real, max real, std real)''')
        conn.commit()
        conn.close()
    def open_db(self):
        self.conn = sqlite3.connect(self.db_file)
    def close_db(self):
        self.conn.close()
    def update_db(self, ST, counters_list, timestamp, run_id, host_id, version, speed=False):
        if not os.path.isfile(self.db_file):
            sys.stderr.write("'%s' is not a file\n" % (db_file))
            sys.exit(1)
        res_mean = ST.mean(counters_list, speed=speed)
        res_max = ST.max(counters_list, speed=speed)
        res_min = ST.min(counters_list, speed=speed)
        res_std = ST.std(counters_list, speed=speed)
        vcounters = []
        for key in res_mean.keys():
            vcounters.append((timestamp, run_id, host_id, version, key,
                res_min[key], res_mean[key], res_max[key], res_std[key]))
        conn = sqlite3.connect(self.db_file)
        conn.executemany("INSERT INTO counters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", vcounters)
        conn.commit()
        conn.close()
    def get_counters(self, value=['timestamp', 'mean'], order_by=['timestamp'], counter=None, run=None, version=None, host=None):
        self.open_db()
        params = {}
        if counter != None:
            params['counter'] = counter
        if run != None:
            params['run_id'] = run
        if version != None:
            params['version'] = version
        if host != None:
            params['host_id'] = host
        if len(params) == 0:
            query_string = 'SELECT %s FROM counters' % (','.join(value))
        else:
            query_string = 'SELECT %s FROM counters WHERE ' % (','.join(value))
        params_value = []
        for key in params.keys():
            query_string += '%s=? AND' % (key)
            params_value.append(params[key])
        query_string = query_string.strip(' AND')
        query_string += ' ORDER BY %s' % (','.join(order_by))
        c = self.conn.cursor()
        c.execute(query_string, params_value)
        result = c.fetchall()
        self.close_db()
        return result
