# Hi Peeps,
# I have a python function that looks through millions of key value relationships in a dictionary and tries to find matching keys/values in other dicts.  If it finds a mat,, it will add 1 to a counter..  It looks like this.
# 
---
Av_T0 = {'key1':'1', 'key2':'20', 'key3':'300'}
pairs_dict = {'key1':'1', 'key4':'4000', 'key3':'300'}
sample_name = 'Av11_pair_one'
coverage_dict = {'key1':['1', '10'], 'key3':['300', '3'], 'key5':'50000'}
min_cov_value = 10
table_position = 0

---
def collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a
    
def collect_hits_0a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a

def collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict):
    allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    return_dict['allelic_count'] = allelic_count    
    return allelic_count

def collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict):
    non_allelic_count = 0
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    return_dict['non_allelic_count'] = non_allelic_count

a = []
a.append(sample_name + "," + str(collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)) + "," + str(collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)))
a

def collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key):
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key):
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a


# Could you give me an idea of how I might parallelize this function??
# Thanks,
# Joe

def collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys)
    
    allelic_count =  [k for k in allelic if (int(coverage_dict[k][table_position]) > min_cov_value)]
    
    
    # print allelic
    # for k in allelic:
    #     print k
    #     print coverage_dict[k][table_position]
    #     print int(coverage_dict[k][table_position]) > min_cov_value
    
    
    # allelic_count = len(allelic)
    a.append(sample_name + "," + str(len(allelic_count)) + "," + str(non_allelic_count))
    
    # return a    
    return a
    
def collect_hits_2a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    print "allelic = "
    print allelic
    allelic_count =  len(allelic)
    
    non_allelic_count = 0 
    #TODO: not in! set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    
    """
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
    """
    a.append(sample_name + "," + str(len(allelic_count)) + "," + str(non_allelic_count))
    
    # return a    
    return a
        
def collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    
    return a

def collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    allelic_count_l = [key for key in pairs_dict.keys() if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value]
    allelic_count = len(allelic_count_l)
    
    non_allelic_count_l = [key for key in coverage_dict.keys() if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value]
    non_allelic_count = len(non_allelic_count_l)
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    
    return a

*) todo create subdict first by int(coverage_dict[key][table_position]) > min_cov_value

    # coverage_dict_ok = {k: coverage_dict[k] for k in coverage_dict.keys() if }
    # dictionary['C1'] = [x+1 for x in dictionary['C1']]
    #
    # coverage_dict_ok = {k: v for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)}
    # >>> for k, v in coverage_dict.items():
    # ...     for x in v:
    # ...             if int(x) > int(min_cov_value):
    # ...                     print "URA"
    # ...                     print x
    # -----
    
    coverage_dict_ok_keys = []
    """
    for tag in tags:
        for entry in entries:
            if tag in entry:
                result.extend(entry)
    
    [entry for tag in tags for entry in entries if tag in entry]
    for k, v in coverage_dict.items():
        for x in v:
                if int(x) > int(min_cov_value):
                        coverage_dict_ok_keys.append(k)
    
    """
    
def collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
                   
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    # allelic_count_l = [key for key in pairs_dict.keys() if key in coverage_dict.keys() and key in Av_T0.keys() and key in coverage_dict_ok_keys]
    # allelic_count = len(allelic_count_l)
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    # print "allelic = "
    # print allelic
    allelic_count =  len(allelic)
    
    non_allelic_count_l = [key for key in coverage_dict.keys() if key not in pairs_dict.keys() and key in Av_T0.keys() and key in coverage_dict_ok_keys]
    non_allelic_count = len(non_allelic_count_l)
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a

def collect_hits_6(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    
    for key in set(coverage_dict_ok_keys).intersection(Av_T0_keys).intersection(coverage_dict_keys):
        if key in pairs_dict_keys:
            allelic_count += 1
        if key not in pairs_dict_keys: 
            non_allelic_count += 1
            
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a


inters_0 = collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_1 = collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_2 = collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_3 = collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_4 = collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_5 = collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)

print(timeit.timeit("collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
48.6235201359
64.53489995
58.5784578323
51.895152092
54.4317700863

print(timeit.timeit("collect_hits_0a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0a, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
66.6070878506
63.4970169067
62.4234759808
64.34131217

print(timeit.timeit("collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_2, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
53.0215709209
54.4635019302

print(timeit.timeit("collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_3, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
64.663351059

print(timeit.timeit("collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_4, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
64.3443729877

print(timeit.timeit("collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_5, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
158.822649956

print(timeit.timeit("collect_hits_6(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_6, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
219.051295996


from multiprocessing import Pool
pool = Pool()
result1 = pool.apply_async(collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)

args = (Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
results = pool.map(collect_hits_01(), args)
from multiprocessing import Process


if __name__ == '__main__':
    Process(target=collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)).start()
    Process(target=collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)).start()


if __name__ == '__main__':
    info('main line')
    p = Process(target=collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))
    p.start()
    p.join()


from multiprocessing import Process

def f(name, text):
    print 'hello', name, text

if __name__ == '__main__':
    p = Process(target=f, args=('bob', 'UUUU',))
    p.start()
    p.join()


if __name__ == '__main__':
    p = Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position,))
    p.start()
    p.join()

from multiprocessing import Process, Manager
import time

if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    durs = []
    
    for i in xrange(1000):    
        start = time.time()
        Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        Process(target=collect_hits_02, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        dur = time.time() - start
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)
    
    for i in xrange(1000):    
        start = time.time()
        collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
        dur = time.time() - start
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)
    
    
    
    a = []
    a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
    a


print(timeit.timeit("Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
=====


pairs_dict = {'GSADVT00027351001_1894': ['1894', 'T', 'A'], 'GSADVT00027990001_479': ['479', 'C', 'T'], 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
Av_T0 = { 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
'Av11_pair_one' = text that I append to output
coverage_dict = {'GSADVT00000104001_410': ['15', '8', '6', '3', '2', '6', '1', '0', '2', '14', '14', '3'], 'GSADVT00000102001_2178': ['0', '1', '0', '1', '0', '3', '1', '0', '0', '4', '1', '4'], 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}

pairs_positions_dict_one = {'GSADVT00000104001_410': ['15', '8', '6', '3', '2', '6', '1', '0', '2', '14', '14', '3'], 'GSADVT00000102001_2178': ['0', '1', '0', '1', '0', '3', '1', '0', '0', '4', '1', '4']}
coverage_dict

===
multi 01 & 02
average time 6805.69720268 us
average time 6511.41142845 us
0
average time 3262.75098324 us
===
import random, string
def randomword(length):
   return ''.join(random.choice(string.uppercase) for i in range(6)) + ''.join(random.choice(string.digits) for i in range(length-6)) + "_" + ''.join(random.choice(string.digits) for i in range(4))

randomword(17)
'bxvgnlwliuidjxtou'

s=string.lowercase+string.digits

from faker import Faker
fake = Faker()

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class MyProvider(BaseProvider):
    def foo(self):
        return 'bar'

# then add new provider to faker instance
fake.add_provider(MyProvider)

# now you can use:
fake.foo()
> 'bar'

class MyProvider(BaseProvider):
    def key_name(self):
        return 'GSADVT' + ''.join(random.choice(string.digits) for i in range(11)) + "_" + ''.join(random.choice(string.digits) for i in range(4))

fake.add_provider(MyProvider)
>>> 
>>> fake.key_name()
'GSADVT49715372880_2519'

https://github.com/joke2k/faker

from collections import defaultdict
big_pairs_dict = defaultdict(list)
for _ in range(0, 10):
  big_pairs_dict[fake.key_name()] = fake.pylist(nb_elements=10, variable_nb_elements=True, "Numbers", "String")
  
pairs_dict

with open('pairs_dict.json', 'w') as f:
    json.dump(big_pairs_dict, f)


from bson import json_util
import json


if not value_types:
    value_types = ['str', 'str', 'str', 'str', 'float', 'int', 'int', 'decimal', 'date_time', 'uri', 'email']
    
value_types = ['int', 'str', 'int', 'str', 'str', 'float', 'int', 'int', 'decimal', 'float', 'decimal', 'decimal']

 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'],

===
import random, string
from collections import defaultdict
from bson import json_util
import json

from faker import Faker
fake = Faker()
from faker.providers import BaseProvider

big_pairs_dict = defaultdict(list)

value_types = ['int', 'str', 'int', 'str', 'str', 'float', 'int', 'int', 'float', 'float', 'float', 'float']

class MyProvider(BaseProvider):
    def key_name(self):
        return 'GSADVT' + ''.join(random.choice(string.digits) for i in range(11)) + "_" + ''.join(random.choice(string.digits) for i in range(4))

fake.add_provider(MyProvider)

for _ in range(0, 2):
    big_pairs_dict[fake.key_name()] = fake.pylist(1000, True, *value_types)

with open('pairs_dict.json', 'w') as f:
    json.dump(big_pairs_dict, f)
---
 pairs_dict = {'GSADVT00027351001_1894': ['1894', 'T', 'A'],
  'GSADVT00027990001_479': ['479', 'C', 'T'],
  'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'],
  'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
 
 z=pairs_dict.copy()
 z.update(big_pairs_dict)
 
 with open('pairs_dict.json', 'w') as f:
     json.dump(z, f)

Av_T0 = { 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
z=Av_T0.copy()
z.update(big_pairs_dict)

with open('Av_T0.json', 'w') as f:
    json.dump(z, f)
---
coverage_dict = {'GSADVT00005150001_2582': ['15', '8', '6', '3', '2', '6', '1', '0', '2', '14', '14', '3'], 'GSADVT00000102001_2178': ['0', '1', '0', '1', '0', '3', '1', '0', '0', '4', '1', '4']}

value_types = ['int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int']
big_coverage_dict = defaultdict(list)

for _ in range(0, 2):
    big_coverage_dict[fake.key_name()] = fake.pylist(1000, True, *value_types)

z=coverage_dict.copy()
z.update(big_coverage_dict)

with open('coverage_dict.json', 'w') as f:
    json.dump(z, f)
===
with open('pairs_dict.json') as pairs_dict_json:
    d = json.load(pairs_dict_json)


import json
with open('pairs_dict.json') as infile:
    o = json.load(infile)
    chunkSize = 3
    for i in xrange(0, len(o), chunkSize):
        with open('file_' + str(i//chunkSize) + '.json', 'w') as outfile:
            json.dump(o[i:i+chunkSize], outfile)
===
t1 = Process(target=f, args=(x,))
t2 = Process(target=f, args=('bob',))

t1.start()
t2.start()

t1.join()
t2.join()
    exit_codes = [p.wait() for p in p1, p2]

===
from itertools import izip_longest

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
This lets you iterate over your tweets in groups of 5000:

for i, group in enumerate(grouper(input_tweets, 5000)):
    with open('outputbatch_{}.json'.format(i), 'w') as outputfile:
        json.dump(list(group), outputfile)
====
=--
def create_get_counts_multi1(return_dict):
    start = time.time()
    with open('pairs_dict.json') as pairs_dict_json:
        pairs_dict = json.load(pairs_dict_json)    
    dur = time.time() - start
    print "json.load(pairs_dict_json)"
    print dur   
    #
    start = time.time()
    pairs_dict_keys    = set(pairs_dict.keys())
    dur = time.time() - start
    print "set(pairs_dict.keys())"
    print dur   
    #
    start = time.time()
    p1 = Process(target=get_allelic_counts1, args=(pairs_dict_keys, return_dict))
    p2 = Process(target=get_non_allelic_counts1, args=(pairs_dict_keys, return_dict))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    dur = time.time() - start
    print "Processes"
    print dur   
    #
    start = time.time()
    a = []
    a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
    return_dict['results'] = a
    dur = time.time() - start
    print a
    print "a.append"
    print dur   
====
done) create original data (/workspace/ashipunova/joe/create_original_data.py)
cd /workspace/ashipunova/joe; time python /workspace/ashipunova/joe/create_original_data.py; mail_done
real    129m51.097s

*) create partial data

*) split subdata

min_cov_value = 10
table_position = 0
sample_name = 'Av11_pair_one'

def make_av_t0_inters_coverage(Av_T0, coverage_dict):
    av_t0_inters_coverage = set(set(Av_T0.keys()).intersection(coverage_dict.keys()))
    with open('av_t0_inters_coverage.json', 'w') as f:
        json.dump(list(av_t0_inters_coverage), f)

def make_coverage_dict_ok_keys(coverage_dict, min_cov_value):
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    with open('coverage_dict_ok_keys.json', 'w') as f:
        json.dump(list(set(coverage_dict_ok_keys)), f)

def make_av_t0_inters_coverage_inters_coverage_dict_ok(coverage_dict_ok_keys, av_t0_inters_coverage):
    av_t0_inters_coverage_inters_coverage_dict_ok = set(coverage_dict_ok_keys).intersection(av_t0_inters_coverage)
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json', 'w') as f:
        json.dump(list(set(av_t0_inters_coverage_inters_coverage_dict_ok)), f)

def collect_hits_7(sample_name, min_cov_value, table_position):
    # start = time.time()
    # with open('pairs_dict.json') as pairs_dict_json:
    #     pairs_dict = json.load(pairs_dict_json)
    # with open('coverage_dict.json') as coverage_dict_json:
    #     coverage_dict = json.load(coverage_dict_json)
    # with open('Av_T0.json') as Av_T0_json:
    #     Av_T0 = json.load(Av_T0_json)
    # p1 = Process(target=make_av_t0_inters_coverage, args=(Av_T0, coverage_dict))
    # p2 = Process(target=make_coverage_dict_ok_keys, args=(coverage_dict, min_cov_value))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    with open('coverage_dict_ok_keys.json') as coverage_dict_ok_keys_json:
        coverage_dict_ok_keys = json.load(coverage_dict_ok_keys_json)
    with open('av_t0_inters_coverage.json') as av_t0_inters_coverage_json:
        av_t0_inters_coverage = json.load(av_t0_inters_coverage_json)
    make_av_t0_inters_coverage_inters_coverage_dict_ok(coverage_dict_ok_keys, av_t0_inters_coverage)
    # with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
    #     av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    # dur = time.time() - start
    # # print dur
    # allelic_count = 0
    # a = []
    # non_allelic_count = 0
    # pairs_dict_keys    = set(pairs_dict.keys())
    # for key in av_t0_inters_coverage_inters_coverage_dict_ok:
    #     if key in pairs_dict_keys:
    #         allelic_count += 1
    #     if key not in pairs_dict_keys:
    #         non_allelic_count += 1
    # a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    # return a


def collect_hits_7(sample_name, min_cov_value, table_position):
    with open('coverage_dict_ok_keys.json') as coverage_dict_ok_keys_json:
        coverage_dict_ok_keys = json.load(coverage_dict_ok_keys_json)
    with open('av_t0_inters_coverage.json') as av_t0_inters_coverage_json:
        av_t0_inters_coverage = json.load(av_t0_inters_coverage_json)
    make_av_t0_inters_coverage_inters_coverage_dict_ok(coverage_dict_ok_keys, av_t0_inters_coverage)

start = time.time()
collect_hits_7(sample_name, min_cov_value, table_position)
dur = time.time() - start
print dur
0.424619913101


def get_allelic_counts(pairs_dict_keys, return_dict):
    allelic_count = 0
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
        av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    allelic_count = 0
    for key in av_t0_inters_coverage_inters_coverage_dict_ok:
        if key in pairs_dict_keys:
            allelic_count += 1
    # check if intersection len is faster
    return_dict['allelic_count'] = allelic_count

def get_non_allelic_counts(pairs_dict_keys, return_dict):
    non_allelic_count = 0
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
        av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    for key in av_t0_inters_coverage_inters_coverage_dict_ok:
        if key not in pairs_dict_keys:
            non_allelic_count += 1
    print non_allelic_count
    # check if intersection len is faster
    return_dict['non_allelic_count'] = non_allelic_count
    
----
def get_allelic_counts1(pairs_dict_keys, return_dict):
    allelic_count = 0
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
        av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    allelic_count = 0
    allelic = set(av_t0_inters_coverage_inters_coverage_dict_ok).intersection(set(pairs_dict_keys))
    allelic_count =  len(allelic)
    #
    return_dict['allelic_count'] = allelic_count

def get_non_allelic_counts1(pairs_dict_keys, return_dict):
    non_allelic_count = 0
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
        av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    allelic_count = 0
    non_allelic = set(pairs_dict_keys) - set(av_t0_inters_coverage_inters_coverage_dict_ok)
    
    # non_allelic_count_l = [key for key in coverage_dict.keys() if key not in pairs_dict.keys() and key in Av_T0.keys() and key in coverage_dict_ok_keys]
    non_allelic_count = len(non_allelic)
    
    return_dict['non_allelic_count'] = non_allelic_count
    
----
def create_get_counts_multi(return_dict):
    dur = 0    
    start = time.time()
    with open('pairs_dict.json') as pairs_dict_json:
        pairs_dict = json.load(pairs_dict_json)    
    dur = time.time() - start
    print "json.load(pairs_dict_json)"
    print dur   
    #
    dur = 0    
    start = time.time()
    pairs_dict_keys    = set(pairs_dict.keys())
    dur = time.time() - start
    print "set(pairs_dict.keys())"
    print dur   
    #
    dur = 0    
    start = time.time()
    p1 = Process(target=get_allelic_counts, args=(pairs_dict_keys, return_dict))
    p2 = Process(target=get_non_allelic_counts, args=(pairs_dict_keys, return_dict))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    dur = time.time() - start
    print "Processes"
    print dur   
    #
    dur = 0    
    start = time.time()
    a = []
    a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
    return_dict['results'] = a
    dur = time.time() - start
    print a
    print "a.append"
    print dur   


if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    # 
    start = time.time()
    create_get_counts_multi1(return_dict)
    dur = time.time() - start
    print dur
    print return_dict
json.load(pairs_dict_json)
303.067904949
set(pairs_dict.keys())
2.071352005
Processes
19.4326558113
['Av11_pair_one,2,5000002']
a.append
0.0229640007019
350.968198061
{'non_allelic_count': 5000002, 'allelic_count': 2, 'results': ['Av11_pair_one,2,5000002']}


json.load(pairs_dict_json)
9.33207607269
set(pairs_dict.keys())
0.183407068253
Processes
0.594051122665
['Av11_pair_one,1,500003']
a.append
0.00127410888672
11.1398279667
11.072217226

json.load(pairs_dict_json)
108.527834177
set(pairs_dict.keys())
2.07861304283
Processes
16.078343153
['Av11_pair_one,2,5000002']
a.append
0.167136907578
150.721369982
{'non_allelic_count': 5000002, 'allelic_count': 2, 'results': ['Av11_pair_one,2,5000002']}


{'non_allelic_count': 500003, 'allelic_count': 1, 'results': ['Av11_pair_one,1,500003']}

if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    # 
    start = time.time()
    create_get_counts_multi(return_dict)
    dur = time.time() - start
    print dur
    print return_dict
json.load(pairs_dict_json)
8.86399292946
set(pairs_dict.keys())
0.185638189316
Processes
0.277464866638
a.append
0.00126194953918
10.3748760223
9.78013801575
9.60346508026

*) python scripts to use partial data
def create_sub_data():
    with open('pairs_dict.json') as pairs_dict_json:
        pairs_dict = json.load(pairs_dict_json)
    with open('coverage_dict.json') as coverage_dict_json:
        coverage_dict = json.load(coverage_dict_json)
    with open('Av_T0.json') as Av_T0_json:
        Av_T0 = json.load(Av_T0_json)
    p1 = Process(target=make_av_t0_inters_coverage, args=(Av_T0, coverage_dict))
    p2 = Process(target=make_coverage_dict_ok_keys, args=(coverage_dict, min_cov_value))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

start = time.time()
create_sub_data()
dur = time.time() - start
print dur
61.2140572071

*) get non_allelic_count as len - allelic_count

*) create shell script to go over partial data


===
print(timeit.timeit("collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=100))

print(timeit.timeit("collect_hits_7(sample_name, min_cov_value, table_position)", setup="from __main__ import collect_hits_7, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=100))

cd /workspace/ashipunova/joe; time python /workspace/ashipunova/joe/create_original_data.py; mail_done
rocket

---
# if __name__ == '__main__':
#     manager = Manager()
#     return_dict = manager.dict()
#     dur = 0
#
#     start = time.time()
#     Process(target=get_allelic_counts, args=().start()
#     Process(target=get_non_allelic_counts, args=()).start()
#     dur = time.time() - start
#     print int(dur)
#
#     a = []
#     a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
#     a
===
~$ cd /workspace/ashipunova/joe; time python /workspace/ashipunova/joe/create_original_data.py; mail_done
real    12m40.784s

=== start ===
import json
from multiprocessing import Process, Manager
import time

min_cov_value = 10
table_position = 0
sample_name = 'Av11_pair_one'

def make_av_t0_inters_coverage(Av_T0, coverage_dict):
    av_t0_inters_coverage = set(set(Av_T0.keys()).intersection(coverage_dict.keys()))
    with open('av_t0_inters_coverage.json', 'w') as f:
        json.dump(list(av_t0_inters_coverage), f)

def make_coverage_dict_ok_keys(coverage_dict, min_cov_value):
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    with open('coverage_dict_ok_keys.json', 'w') as f:
        json.dump(list(set(coverage_dict_ok_keys)), f)

def make_av_t0_inters_coverage_inters_coverage_dict_ok(coverage_dict_ok_keys, av_t0_inters_coverage):
    av_t0_inters_coverage_inters_coverage_dict_ok = set(coverage_dict_ok_keys).intersection(av_t0_inters_coverage)
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json', 'w') as f:
        json.dump(list(set(av_t0_inters_coverage_inters_coverage_dict_ok)), f)

def create_sub_data():
    with open('pairs_dict.json') as pairs_dict_json:
        pairs_dict = json.load(pairs_dict_json)
    with open('coverage_dict.json') as coverage_dict_json:
        coverage_dict = json.load(coverage_dict_json)
    with open('Av_T0.json') as Av_T0_json:
        Av_T0 = json.load(Av_T0_json)
    p1 = Process(target=make_av_t0_inters_coverage, args=(Av_T0, coverage_dict))
    p2 = Process(target=make_coverage_dict_ok_keys, args=(coverage_dict, min_cov_value))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

start = time.time()
create_sub_data()
dur = time.time() - start
print dur
669.450684071
# ---
# or create_sub_data_separately and run the second process for all min_cov_value with qsub
# def create_sub_data_separately():
#     with open('pairs_dict.json') as pairs_dict_json:
#         pairs_dict = json.load(pairs_dict_json)
#     with open('coverage_dict.json') as coverage_dict_json:
#         coverage_dict = json.load(coverage_dict_json)
#     with open('Av_T0.json') as Av_T0_json:
#         Av_T0 = json.load(Av_T0_json)
#     p1 = Process(target=make_av_t0_inters_coverage, args=(Av_T0, coverage_dict))
#     p2 = Process(target=make_coverage_dict_ok_keys, args=(coverage_dict, min_cov_value))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
# 
# 
# ---
def create_sub_data_sep_3():
    with open('coverage_dict_ok_keys.json') as coverage_dict_ok_keys_json:
        coverage_dict_ok_keys = json.load(coverage_dict_ok_keys_json)
    with open('av_t0_inters_coverage.json') as av_t0_inters_coverage_json:
        av_t0_inters_coverage = json.load(av_t0_inters_coverage_json)
    make_av_t0_inters_coverage_inters_coverage_dict_ok(coverage_dict_ok_keys, av_t0_inters_coverage)

start = time.time()
create_sub_data_sep_3()
dur = time.time() - start
print dur
5.9403719902


def get_allelic_counts2(pairs_dict_keys):
    with open('av_t0_inters_coverage_inters_coverage_dict_ok.json') as av_t0_inters_coverage_inters_coverage_dict_ok_json:
        av_t0_inters_coverage_inters_coverage_dict_ok = json.load(av_t0_inters_coverage_inters_coverage_dict_ok_json)
    allelic = set(av_t0_inters_coverage_inters_coverage_dict_ok).intersection(pairs_dict_keys)
    return len(allelic)

def get_non_allelic_counts2(pairs_dict_keys, allelic_count):
    return len(pairs_dict_keys) - int(allelic_count)

def create_get_counts_multi2():
    dur = 0
    start = time.time()
    with open('pairs_dict.json') as pairs_dict_json:
        pairs_dict = json.load(pairs_dict_json)    
    dur = time.time() - start
    print "json.load(pairs_dict_json)"
    print dur   
    #
    dur = 0
    start = time.time()
    pairs_dict_keys    = set(pairs_dict.keys())
    dur = time.time() - start
    print "set(pairs_dict.keys())"
    print dur   
    #
    dur = 0
    start = time.time()
    allelic_count = 0    
    allelic_count = get_allelic_counts2(pairs_dict_keys)
    dur = time.time() - start
    print "get_allelic_counts2"
    print dur   
    #
    dur = 0
    start = time.time()
    non_allelic_count = 0
    non_allelic_count = get_non_allelic_counts2(pairs_dict_keys, allelic_count)
    dur = time.time() - start
    print "get_non_allelic_counts2"
    print dur   
    #
    dur = 0
    start = time.time()
    results = []
    results.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    dur = time.time() - start
    # print results
    print "results.append"
    print dur
    return results
    
if __name__ == '__main__':
    start = time.time()
    results = create_get_counts_multi2()
    dur = time.time() - start
    print dur
    print results

    json.load(pairs_dict_json)
    1383.25313711
    set(pairs_dict.keys())
    2.96267580986
    get_allelic_counts2
    1.69007396698
    get_non_allelic_counts2
    0.00461292266846
    ['Av11_pair_one,2,0']
    a.append
    0.000157117843628
    1408.89393306
    {'non_allelic_count': 0, 'allelic_count': 2, 'results': ['Av11_pair_one,2,0']}

    json.load(pairs_dict_json)
    973.843216896
    set(pairs_dict.keys())
    2.1346449852

    json.load(pairs_dict_json)
    495.948715925
    set(pairs_dict.keys())
    2.24417304993
    get_allelic_counts2
    0.0299081802368

    json.load(pairs_dict_json)
    165.095906019
    set(pairs_dict.keys())
    2.00420308113
    get_allelic_counts2
    0.0039370059967
    get_non_allelic_counts2
    6.19888305664e-06
    ['Av11_pair_one,2,5000002']
    results.append
    0.00167894363403
    188.319638968
    ['Av11_pair_one,2,5000002']

    json.load(pairs_dict_json)
    1631.57953405
    set(pairs_dict.keys())
    2.40771985054
    get_allelic_counts2
    0.00116920471191
    get_non_allelic_counts2
    1.4066696167e-05
    results.append
    0.000362157821655
    >>> dur = time.time() - start
    >>> print dur
    1656.97435808
    >>> print results
    ['Av11_pair_one,2,5000002']


json.load(pairs_dict_json)
156.543590069
set(pairs_dict.keys())
2.2940299511
get_allelic_counts2
0.000720024108887
get_non_allelic_counts2
3.81469726562e-06
results.append
5.96046447754e-06
>>> dur = time.time() - start
>>> print dur
181.494456053
>>> print results
['Av11_pair_one,2,5000002']

