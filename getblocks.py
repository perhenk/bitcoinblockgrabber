"""
Henter ut data fra BitCoin blokkkjeden og lager en CSV fil

NB: Kjøres i Python3 

@author Per-Henrik Kvalnes
"""
import csv
import datetime
from blockchain import blockexplorer

# Sett opp klart til skriving til CSV fil
fieldnames = ['block_hash', 'block_height','size','relayed_by','datetime','timestamp','tx_index','from_address','to_address', 'from_value','to_value']
f = open('test2.csv','w')
csvf = csv.DictWriter(f,fieldnames=fieldnames)
csvf.writeheader()

# åpne en liste med blokker
blocklist = open('blocklist.txt', 'r')

for block_hash in blocklist:

    # Hent blokk
    block = blockexplorer.get_block(block_hash)
    
    # Travaser alle transaskjoner i blokkken
    for t in block.transactions:

        # Gå gjennom adresser beløp inn
        for inn in t.inputs:
            # Gå gjennom adresser beløp ut
            for out in t.outputs:
                # Prøvd å lage en skrive en rad i CSV. Hvis ikke igonrer. 
                try:
                    row = {}
                    row["block_hash"] = block_hash
                    row["block_height"] = t.block_height
                    row["size"] = t.size
                    row["relayed_by"] = t.relayed_by
                    row["datetime"] =  datetime.datetime.fromtimestamp(t.time).strftime('%Y-%m-%d %H:%M:%S')
                    row["timestamp"] =  t.time
                    row["tx_index"] = t.tx_index
                    row["to_address"] = out.address
                    row["to_value"] = out.value / (10.0**8)

                    if inn.sequence != 0:
                        row["from_address"] = inn.address
                        row["from_value"] = inn.value / (10.0**8.0)
                    else: print(inn.__dict__)

                    csvf.writerow(row)


                except:
                    print("Can not write this block")
                    print(inn.__dict__)

# Lukk file

f.close()
















