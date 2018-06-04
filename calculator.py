#! /usr/bin/env python3

import sys
import csv
import getopt
from configparser import ConfigParser 
import time

class Args(object):
    def __init__(self):
       # args = sys.argv[1:]
       # self.c = args[args.index('-c')+1]
       # self.d = args[args.index('-d')+1]
       # self.o = args[args.index('-o')+1]
        self.args = self._read_args()

    def _read_args(self):
        
        data={}
        try:
            opts,args = getopt.getopt(sys.argv[1:],"hC:c:d:o:")
        except getopt.GetoptError:
            print('python3 calculatory.py -c <conf> -d <userdata> -o <output>')
            sys.exit(2)

        for opt,arg in opts:
            if opt == '-h':
                print('python3 calculatory.py -c <conf> -d <userdata> -o <output>')
                sys.exit()
            elif opt == '-C':
                data['-C'] = arg
            elif opt == '-c':
                data['-c'] = arg
            elif opt == '-d':
                data['-d'] = arg
            elif opt == '-o':
                data['-o'] = arg
        if '-C' not in data:
            data['-C'] = 'DEFAULT'
        if len(data) != 4:
            print('it\'s wrong,you need 3 args,like python3 calculatory.py -c <conf> -d <userdata> -o <output>')
            sys.exit()
        return data

args = Args().args

class City():
    def __init__(self):
        self.config = self._read_city()
    def _read_city(self):
        parser = ConfigParser()
        city = args['-C']
        parser.read(args['-c'])
        config = {}
        for x in parser[city]:
            config[x] = parser.getfloat(city,x)
        
        return config

ctax = City().config

class Config(object):
    def __init__(self):
        self.config = self._read_config()
    def _read_config(self):
        config = {'s': 0}
        try:
            with open(args[1]) as f:
                data = f.readlines()
            for con in data:
                con1, con2 = con.strip().split('=')
                con1 = con1.strip()
                con2 = con2.strip()
                if con1 == 'JiShuL' or con1 == 'JiShuH':
                    config[con1] = float(con2)
                else:
                    config['s'] += float(con2)
        except Exception as e:
            print ('what the fuck!config',e)

        return config

#config = Config().config

class UserData(object):
    def __init__(self):
        with open(args['-d']) as f:
            self.data = list(csv.reader(f))

data = UserData().data

def cal(salary):
    salary = int(salary)
    bili = sum(ctax.values())-ctax['jishul']-ctax['jishuh']
    shebao = salary * bili
    if salary <= ctax['jishul']:
        shebao = ctax['jishul'] * bili
    if salary >= ctax['jishuh']:
        shebao = ctax['jishuh'] * bili
    x = salary - shebao - 3500
    if x <= 0:
        tax = 0
    elif x <= 1500:
        tax = x * 0.03
    elif x<= 4500:
        tax = x* 0.1 -105
    elif x<= 9000:
        tax = x * 0.2 -555
    elif x <= 35000:
        tax = x * 0.25 -1005
    elif x <= 55000:
        tax = x * 0.3 - 2775
    elif x <= 80000:
        tax = x * 0.35 - 5505
    else:
        tax = x * 0.45 - 13505
    return [format(salary,'.2f'), format(shebao, '.2f'), format(tax,'.2f'),format(salary-shebao-tax,'.2f')]
    
if __name__ == '__main__':
    with open(args['-o'], 'w') as f:
        for num, salary in data:
            x = cal(salary)
            x.insert(0, num)
            x.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            csv.writer(f).writerow(x)
