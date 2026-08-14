import sys
import time


def jalanin_lirik () :
    lirik = [
                ("Bila kau berkenan",0.2),
                ("Biarkanku di sampingmu",0.2),
                ("Berkuranglah satu jiwa yang sepi",0.2),
                ("Ini semua bukan salahmu",0.2),
                ("Punya magis perekat yang sekuat itu",0.1),
                ("Dari lahir sudah begitu",0.2),
                ("Maafkan, oh-uh-uh",0.1),
                ("Ini semua bukan salahmu",0.1),
                ("Punya magis perekat yang sekuat itu",0.1),
                ("Dari lahir sudah begitu",0.1),
                ("Maafkan",0.1),
                ("Hm-mm",0.1),
                ("Aku jatuh suka",0.1),
                ("Aku jatuh suka",0.1)
    ]

    delay = [0.5, 2, 4, 1, 1, 1, 4, 2, 3, 2, 3, 2, 8, 2]


    time.sleep(0.1)
    for i, (baris_lagu, delay_karakter) in enumerate(lirik):
        for karakter in baris_lagu:
            print(karakter, end='')
            sys.stdout.flush()
            
            time.sleep(delay_karakter)

        print()
        time.sleep(delay[i])
jalanin_lirik()
