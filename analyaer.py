import chipwhisperer.analyzer as cwa
import chipwhisperer as cw
import sys
import numpy as np
import matplotlib.pylab as plt



print("✔️ OK to continue!")



proj = cw.openProject("rhme2016_project_piece_of_scacke.cwp")

resync_traces = cwa.preprocessing.ResyncSAD(proj)
resync_traces.ref_trace = 0
resync_traces.target_window = (1400,1600)
resync_traces.max_shift = 500

resync_analyzer = resync_traces.preprocess()



leak_model = cwa.leakage_models.sbox_output
attack = cwa.cpa(resync_analyzer, leak_model)
attack.point_range=(0,12000)


plt.plot(resync_analyzer.waves[0],'r')
plt.plot(resync_analyzer.waves[1],'g')
plt.plot(resync_analyzer.waves[2],'b')
plt.show();

results = attack.run(None,10)
print(results.best_guesses)
print(results)
print(results.key_guess())
