import chipwhisperer.analyzer as cwa
import chipwhisperer as cw
import sys
import numpy as np
import matplotlib.pylab as plt



trace_array=np.load("2500_traces_buona.npy")
textin_array=np.load("2500_texts_buona.npy")

print(np.sum(trace_array[5]))

plt.plot(trace_array[0])
plt.plot(trace_array[1])
plt.plot(trace_array[2])
plt.plot(trace_array[3])
plt.plot(trace_array[5])
plt.show()

proj = cw.create_project("test_aes_own_trace.cwp",overwrite=True)


#key=np.random.randint(10,size = 16)
for i in range(len(trace_array)):
    if len(textin_array[i]) == 16 :
        trace = cw.Trace(trace_array[i],textin_array[i] , None, '\x50'*16)
        proj.traces.append(trace)

print("[+] Traces caricate ",len(proj.traces))
print("[+] Traces totali ",len(trace_array))



proj.save()

print("[*] Plotting unalligned traces... ")

plt.plot(proj.waves[2])
plt.show()

for i in range(0,5):
    plt.plot(proj.waves[i])
    print(np.sum(proj.waves[i]))

plt.show();


print("[*] Traces loaded...")
print("[*] SAD running")
#############################
# PRE - PROCESSING
#############################
resync_traces = cwa.preprocessing.ResyncSAD(proj)
resync_traces.ref_trace = 0
#resync_traces.target_window = (1650,1800)
resync_traces.target_window = (5200,6400)
resync_traces.max_shift =100
resync_analyzer = resync_traces.preprocess()
print("[*] Number of traces after reallignement ",len(resync_analyzer.waves))

 ##########plotting



print("[*] Plotting alligned traces... ")

for i in range(0,4):
    plt.plot(resync_analyzer.waves[i])
plt.show();

##################àà
#attack configuration
##########
print("[*] Attack running ")

leak_model = cwa.leakage_models.sbox_output
attack = cwa.cpa(resync_analyzer, leak_model)
#attack.point_range=(15000,250000)
attack.trace_range=(1,50)
#attack.subkey_list=[0,1,2,3,4,5]


results = attack.run(callback=None, update_interval=20)
#####################
results.set_known_key([0xaf, 0x23, 0xd5, 0x45, 0xa0, 0xea, 0xe6, 0xa0, 0x74, 0x65, 0x96, 0xca, 0xce, 0x51, 0xf0, 0xf7])

print(results)
print(results.best_guesses())


print(results.simple_PGE(0))
rec_key2 = []
for bnum in results.find_maximums():
    print("Best Guess = 0x{:02X}, Corr = {}".format(bnum[0][0], bnum[0][2]))
    rec_key2.append(bnum[0][0])

print(rec_key2)
