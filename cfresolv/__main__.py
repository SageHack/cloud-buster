from cf_detect import CF_Detect


if __name__ == "__main__":
    cf = CF_Detect()
    print(cf.in_range('adfasdf'))
    print(cf.in_range(''))
    print(cf.in_range('172.71.255.250'))
    print(cf.in_range('250.71.255.250'))
    print(cf.in_range('2400:cb00::5e:b4da'))
    print(cf.in_range('9400:cb00::5e:b4da'))
