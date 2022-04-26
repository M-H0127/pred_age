import scipy.signal
import numpy as np
from tqdm import tqdm

def evaluate(pred, label, height):
    pred=np.append(pred,0)
    pred=np.append(0,pred)
    age_list,_=scipy.signal.find_peaks(pred, height=height, threshold=None, distance=9, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    if len(age_list)==0:
        age_list=np.array([np.argmax(pred)])
    labelindex = np.array([i for i, x in enumerate(label) if x == max(label)])
    age_mae=0
    for i in age_list:
        i-=1
        min_age = np.min(np.abs(labelindex - i))
        age_mae +=min_age
    age_mae = age_mae/len(age_list)
    num_mae = np.abs(len(labelindex)-len(age_list))
    return age_mae, num_mae
        
def make_thresh(pred_vali, label_vali):
    min_mae=10000
    for t in np.arange(0,1.1,0.1):
        num_mae=0
        for i,j in zip(tqdm(pred_vali),label_vali):
            x=evaluate(i,j,t)
            num_mae += x
        num_mae=num_mae/len(pred_vali)
        print(f"num_mae:{num_mae}")
        if min_mae>num_mae:
            min_mae=num_mae
            ikiti=t
            continue
        break
    print("次の桁")
    min_mae=10000
    for q in np.arange(0,0.11,0.01):
        num_mae=0
        for i,j in zip(tqdm(pred_vali),label_vali):
            _, x=evaluate(i,j,ikiti+q)
            num_mae += x
        num_mae=num_mae/len(pred_vali)
        print(f"num_mae:{num_mae}")
        if min_mae>num_mae:
            min_mae=num_mae
            ikiti2=q
            continue
        break
    if ikiti2==0:
        for q in np.arange(0.01,0.11,0.01):
            num_mae=0
            for i,j in zip(tqdm(pred_vali),label_vali):
                _, x=evaluate(i,j,ikiti-q)
                num_mae += x
            num_mae=num_mae/len(pred_vali)
            print(f"num_mae:{num_mae}")
            if min_mae>num_mae:
                min_mae=num_mae
                ikiti2=-q
                continue
            break
    return ikiti+ikiti2