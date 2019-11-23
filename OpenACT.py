import datetime
import os
import time

save_path='users\\phoneUse_vas'


class Recorder():
    def __init__(self,dataStr):
        dArr=dataStr.split(",")
        self.data=dataStr
        self.dataArr=dArr
        self.type=dArr[0]
        ticksStr=dArr[1]
        self._sepData=None
        self.ticks=datetime.datetime.strptime(ticksStr,"%Y-%m-%d %H:%M:%S")
        self.ticksInSecond=time.mktime(self.ticks.timetuple())
        if "OPEN_ACT"==self.type:
            self.ticksInSecond+=0.5;
        self.ticksDate=self.ticks.date()
        self.secondsInDay=time.mktime(self.ticks.timetuple())-time.mktime(self.ticksDate.timetuple())

    def getSepData(self):
        if self._sepData==None:
            self._sepData=self.dataArr[2].split(";")
        return self._sepData
    def toLine(self):
        if self._sepData!=None:
            sd=';'.join(self._sepData)
            self.dataArr[2]=sd
        s=",".join(self.dataArr)
        return s+"\n"

    # def getType

class RecorderStatus():
    MAX_SECONDS_IN_DAY=24*3600;
    def __init__(self,patientID):
        self.patientID=patientID
        self.dayStatusMap={}
    def checkDate(self,recorder):
        if recorder.ticksDate in self.dayStatusMap.keys():
            if recorder.secondsInDay < self.dayStatusMap[recorder.ticksDate][0] and recorder.secondsInDay>3*3600:
                self.dayStatusMap[recorder.ticksDate][0]=recorder.secondsInDay
            if recorder.secondsInDay > self.dayStatusMap[recorder.ticksDate][1]:
                self.dayStatusMap[recorder.ticksDate][1]=recorder.secondsInDay
            if recorder.secondsInDay < self.dayStatusMap[recorder.ticksDate][2]:
                self.dayStatusMap[recorder.ticksDate][2] = recorder.secondsInDay

        else:
            self.dayStatusMap[recorder.ticksDate]=[recorder.secondsInDay,recorder.secondsInDay,recorder.secondsInDay]


class Correction():
    def __init__(self,pi):
        self.patientInfo=pi
        self.typeKeyArr=[]
        self.resultLst=[]
        self.dataLst=[]
    def wrapResultRec(self,rec,duration):
        rec.type=rec.type+"_2"
        rec.dataArr[0]=rec.type
        return rec
    def check(self,rec):
        if rec.type in self.typeKeyArr:
            self.dataLst.append(rec)
    def correct(self):
        self.dataLst = sorted(self.dataLst, key=lambda k: k.ticksInSecond)

    def addToFileEnd(self,fileName):
        f=open(os.path.join(save_path,fileName),'a',encoding='utf-8')
        for rec in self.resultLst:
            f.write(rec.toLine())
        f.close()

class CorrectOPEN_ACT(Correction):
    def __init__(self,pi):
        super().__init__(pi)
        self.typeKeyArr = ['OPEN_ACT', "CLOSE_ACT"]
        self.maxDurationDict={}
    def getPackage(self,rec):
        return rec.getSepData()[0]
    def wrapResultRec(self,rec,duration):
        rec=super().wrapResultRec(rec,duration)
        rec.getSepData()[2]=str(int(duration))
        return rec
    def correct(self):
        super().correct()
        lastOpenAct=None
        lastCloseAct=None

        _self=self
        def noClosePatch(actObj):
            p=_self.getPackage(actObj)
            if p in self.maxDurationDict.keys():
                _self.resultLst.append(self.wrapResultRec(actObj, self.maxDurationDict[p]))
            else:
                _self.resultLst.append(self.wrapResultRec(actObj, 60))
        def recordMaxDuration(actObj,duration):
            p=_self.getPackage(actObj)
            if p in self.maxDurationDict.keys():
                self.maxDurationDict[p] =  self.maxDurationDict[p]  if self.maxDurationDict[p] > duration else duration
            else:
                self.maxDurationDict[p]=duration
        def addRec(lastOpenAct,duration):
            if duration < 3 * 3600 and duration >= 1 :
                self.resultLst.append(self.wrapResultRec(lastOpenAct, duration))
                recordMaxDuration(lastOpenAct, duration)
            else:
                noClosePatch(lastOpenAct)
        for i in range(0,len(self.dataLst)):
            rec=self.dataLst[i]
            if rec.type=='OPEN_ACT':
                if lastOpenAct==None:
                    lastOpenAct=rec
                else:
                    if self.getPackage(rec)==self.getPackage(lastOpenAct):
                        pass
                    else:
                        if lastCloseAct!=None:
                            duration=lastCloseAct.ticks.timestamp()-lastOpenAct.ticks.timestamp()
                            addRec(lastOpenAct,duration)
                        else:
                            duration=rec.ticks.timestamp()-lastOpenAct.ticks.timestamp()
                            addRec(lastOpenAct,duration)
                        lastOpenAct=rec
                        lastCloseAct=None
            elif rec.type=="CLOSE_ACT":
                lastCloseAct=rec

        duration = self.dataLst[-1].ticks.timestamp() - lastOpenAct.ticks.timestamp()
        addRec(lastOpenAct,duration)

class CorrectScreen(Correction):
    def __init__(self,pi):
        super().__init__(pi)
        self.typeKeyArr=["SCREEN_ACTIVE_TYPE"]
        self.dataLst=[]
        self.result=[]
    def wrapResultRec(self,rec,duration):
        rec=super().wrapResultRec(rec,duration)
        if duration!=None:
            rec.getSepData()[0]=str(int(duration))
        return rec
    def correct(self):
        super().correct()
        lastDate=None
        for i in range(0,len(self.dataLst)):
            rec=self.dataLst[i]
            if rec.secondsInDay>4*3600:
                if lastDate==None or rec.ticksDate!=lastDate:
                    lastDate=rec.ticksDate
                    lastDay=lastDate-datetime.timedelta(1)
                    tS=self.patientInfo.status.dayStatusMap[lastDate]
                    d=0
                    if tS[2]<tS[0] and tS[2]<rec.secondsInDay:
                        d=rec.secondsInDay-tS[2]
                    else:
                        if lastDay in self.patientInfo.status.dayStatusMap.keys():
                            d=rec.secondsInDay+24*3600-self.patientInfo.status.dayStatusMap[lastDay][1]
                        else:
                            d=rec.secondsInDay
                    if d<3600:
                        p=20
                    self.resultLst.append(self.wrapResultRec(rec, d))
                else:
                    self.resultLst.append(self.wrapResultRec(rec,None))
class PatientInfo():
    def __init__(self,patientID):
        self.patientID=patientID
        self.fileName=patientID+"-MobileUseData.csv"
        self.status=RecorderStatus(self.patientID)
        self.cOpen=CorrectOPEN_ACT(self)
        self.cScreen=CorrectScreen(self)
        self.go()
        self.makeResult()
    def go(self):
        f=open(os.path.join(save_path,self.fileName),"r",encoding='utf-8')
        line=f.readline()
        while line!='':
            line=line.replace("\n","")
            rec=Recorder(line)
            self.status.checkDate(rec)
            self.cOpen.check(rec)
            self.cScreen.check(rec)
            line=f.readline()
        f.close()
    def makeResult(self):
        self.cOpen.correct()
        self.cOpen.addToFileEnd(self.fileName)
        self.cScreen.correct()
        self.cScreen.addToFileEnd(self.fileName)


def get_file_list():
    '''
    :return:
    '''
    files = os.listdir(save_path)
    files = sorted(files)
    return files

if __name__ == "__main__":
    names=get_file_list()
    i=0
    for x in names:
        pi=PatientInfo(x[:8])
        print(x[:8])
        print(i)
        i+=1