import csv

players = []

with open('co2022.csv', 'w', newline='') as co2022:
    with open('utrranks.csv', newline='', encoding='utf8') as utrRanks:
            utrReader = csv.DictReader(utrRanks)
            coWriter = csv.writer(co2022, delimiter=' ')
            for row1 in utrReader:
                with open('trnetranks.csv', newline='', encoding='utf8') as trRanks:
                    trReader = csv.DictReader(trRanks)
                    for row2 in trReader:
                        if row1['names'].lower() == row2['name'].lower():
                            players.append(row1['names'])
                            out = f"{len(players)}: {row1['names'][:30]}"
                            for i in range(30 - len(row1['names'][:30])):
                                out += " "
                            out += row1['actual utr']
                            print(out)