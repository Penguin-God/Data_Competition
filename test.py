import os
import math
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Malgun Gothic'

class Region:
    def __init__(self, path):
        self.regionName = path[0] + path[1]
        self.data = pd.read_csv(path, encoding="utf-8")
    
    def Pirvate_GetCategoryDict(self, data, mainName, subName, deadLine = 1):
        mainCategory = set(data[mainName])
        result = {}
        for main in mainCategory:
            result[main] = self.GetCategoryByCount(subName, filter=(data[mainName] == main), deadLine=2)
        return result

    def GetCategoryDict(self, mainName, subName):
        return self.Pirvate_GetCategoryDict(self.data, mainName, subName)

    def GetCategoryDict_HasFilt(self, filt, mainName, subName):
        filter = (self.data[filt[0]] == filt[1])
        return self.Pirvate_GetCategoryDict(self.data[filter], mainName, subName)

    def GetCategoryByCount(self, columnName, filter = True, deadLine = 1):
        dic = {}
        categorys = set(self.data[columnName])

        for i in categorys:
            filt = ((self.data[columnName] == i) & filter)
            dic[i] = len(self.data[filt])
            
        self.HideEtc(dic, deadLine=deadLine)
        return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}

    def HideEtc(self, dic, deadLine = 5):
        total = 0
        for i in dic:
            total += dic[i]
        for i in dic.copy():
            percent = (dic[i] / float(total)) * 100.0
            if(percent <= deadLine):
                if('기타' in dic):
                   dic['기타'] += dic[i]
                else:
                     dic['기타'] = dic[i]
                dic.pop(i, dic[i])
                
                

class GraphDrawer:
    def ShowDetailGraphs(self, dict, type = 'pie', title = ''):
        length = len(dict)
        ySize = round(math.sqrt(length))
        xSize = math.ceil(math.sqrt(length))
        
        fig, axs = plt.subplots(ySize, xSize, figsize=(140, 140), squeeze=False, dpi=120)
        matplotlib.rcParams.update({'font.size': 15})
        #fig.tight_layout()
        currentX = 0
        currentY = 0
        for main in dict:
            if(type == 'bar'):
                self.DrawBar(dict[main], axs[currentY, currentX], main+title)
            elif(type == 'pie'):
                self.DrawPie(dict[main], axs[currentY, currentX], main+title)

            if(currentX < xSize-1):
                currentX += 1
            else:
                currentX = 0
                currentY += 1

        self.Show()

    def ShowRegionGraphs(self, regions, columnName, type = 'bar', deadLine = 1):
        current = 0
        length = len(regions)
        ySize = round(math.sqrt(length))
        xSize = math.ceil(math.sqrt(length))
        fig, axs = plt.subplots(ySize, xSize, figsize=(60,60), squeeze=False, dpi=80)
        matplotlib.rcParams.update({'font.size': 13})

        for i in axs:
            for graph in i:
                if(len(regions) > current):
                    if(type == 'bar'):
                        self.DrawBar(regions[current].GetCategoryByCount(columnName, deadLine=deadLine), graph, regions[current].regionName)
                    elif(type == 'pie'):
                        self.DrawPie(regions[current].GetCategoryByCount(columnName, deadLine=deadLine), graph, regions[current].regionName)
                    current += 1
                else:
                    break 
        self.Show()
        
    def Show(self):
        plt.subplots_adjust(bottom=0.2, left=0.05)
        plt.show()

    def DrawBar(self, dict, ax, title):
        pair = self.DictoinaryToPair(dict)
        ax.bar(pair[0], pair[1])
        ax.set_title(title, fontsize=25)
        ax.tick_params(labelrotation=70)

    def DrawPie(self, dict, ax, title):
        pair = self.DictoinaryToPair(dict)
        ax.set_title(title, fontsize=25)
        ax.pie(pair[1], labels=pair[0], autopct='%.1f%%')

    def DictoinaryToPair(self, dic):
        dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
        categorys = []
        counts = []
        for i in dic:
            categorys.append(i)
            counts.append(dic[i])
        return (categorys, counts)


keyWord = '제주'
regions = []
for i in os.listdir():
    if(keyWord in i):
        regions.append(Region(i))

#GraphDrawer().ShowRegionGraphs(regions, '상권업종대분류명', 'pie', deadLine=3)
#GraphDrawer().ShowRegionGraphs(regions, '상권업종대분류명', 'bar', deadLine=3)

#GraphDrawer().ShowDetailGraphs(regions[0].GetCategoryDict('시군구명', '상권업종대분류명'), 'bar')
GraphDrawer().ShowDetailGraphs(regions[0].GetCategoryDict_HasFilt(['상권업종대분류명', '음식'], '상권업종대분류명', '상권업종소분류명'), type='bar', title = " : 제주도")
