from urllib.request import urlopen
from bs4 import BeautifulSoup

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import pandas as pd

class DeviceManager(Base):
    __tablename__ = 'device_manager'
 
    devnameko = sqlalchemy.Column(sqlalchemy.String(length=500), primary_key=True)
    devnameen = sqlalchemy.Column(sqlalchemy.String(length=500))
    manager = sqlalchemy.Column(sqlalchemy.String(length=500))
    phone = sqlalchemy.Column(sqlalchemy.String(length=500))
 
    def __repr__(self):
        return "<DeviceManager(devnameko='{0}', devnameen='{1}', manager='{2}', phone='{3}')>".format(
                            self.devnameko, self.devnameen, self.manager, self.phone)

engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://root:9907@localhost:3306/test',
    echo=True)

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
 

url = 'http://www.cnucrf.re.kr/EquipList_byKor.asp'

html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

def listToDict(lstA, lstB):
    zippedLst = zip(lstA, lstB)
    op = dict(zippedLst)
    return op


def listToDict4(lstA, lstB, lstC, lstD):
    zippedLst = zip(lstA, lstB, lstC, lstD)
    op = dict(zippedLst)
    return op    


def getDevice():
    device_results = soup.find_all("a")

    lst_device = []
    for dev_tag in device_results:
        if 'EquipView.asp?EquipID=' in dev_tag['href'] and 'viewmode=schedule' not in dev_tag['href']:
            if dev_tag.text != '':
                lst_device.append(dev_tag.text)
    return lst_device


def getDeviceEng():
    device_eng_name = soup.find_all("span")

    lst_dev_eng_name = []
    for dev_eng_tag in device_eng_name:
        try:
            if 'font-weight:normal'==dev_eng_tag['style']:
                lst_dev_eng_name.append(dev_eng_tag.text)
        except:
            pass
    return lst_dev_eng_name


def getWorker():
    worker = soup.find_all("div")

    lst_worker = []
    lst_phone = []
    for worker_tag in worker:
        # print(worker_tag)
        try:
            if 'padding-top' in worker_tag['style']:
                lst_worker.append(worker_tag.text[:worker_tag.text.find('0')])
                lst_phone.append(worker_tag.text[worker_tag.text.find('0'):])
        except:
            pass
    return (lst_worker, lst_phone)


lst_device = getDevice()
lst_dev_eng_name = getDeviceEng()

dict_device = listToDict(lst_device, lst_dev_eng_name)

# for k, v in dict_device.items():
#     print(k, ',', v)


worker = soup.find_all("div")
lst_worker, lst_phone = getWorker()
dict_manager = listToDict(lst_worker, lst_phone)

# for k, v in dict_manager.items():
#     print(k,',', v)

for i in range(len(lst_device)):
    currentmanager = DeviceManager(devnameko=lst_device[i].strip(), devnameen=lst_dev_eng_name[i].strip(), 
        manager=lst_worker[i].strip(), phone=lst_phone[i].strip())
    session.add(currentmanager)

session.commit()