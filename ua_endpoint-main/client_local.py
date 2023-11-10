#%%
import requests
import time
paylod = {
            "file_name": '20231024-0215-OW-UA-stop-0359-size-40000.gz',
            # "r" : True,
            "unixtime_g":f"DMTESTFER2{time.time().replace('.','')}",
            "n":500
            .max_proce
          }

# requests.get('https://us-west1-ice-3victors.cloudfunctions.net/ue_aws_input',params=paylod)
res = requests.get('https://us-west1-ice-3victors.cloudfunctions.net/ue_aws_input',params=paylod)
# res = requests.get('http://localhost:8580',params=paylod)

res.text

# %%
