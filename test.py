from cProfile import label
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
    
    def Pirvate_GetCategoryDict(self, data, mainName, subName):
        mainCategory = set(data[mainName])
        subCategory = set(data[subName])
        result = {}
        for main in mainCategory:
            result[main] = {}
            for sub in subCategory:
                filt = ((data[mainName] == main) & (data[subName] == sub))
                result[main][sub] = len(data[filt])
                
        return result

    def GetCategoryDict(self, mainName, subName):
        return self.Pirvate_GetCategoryDict(self.data, mainName, subName)

    def GetCategoryDict_HasFilt(self, filt, mainName, subName):
        filter = (self.data[filt[0]] == filt[1])
        return self.Pirvate_GetCategoryDict(self.data[filter], mainName, subName)

    def GetCategoryByCount(self, columnName):
        dic = {}
        
        for i in self.data[columnName]:
            if(i in dic):
                dic[i] += 1
            else:
                dic[i] = 1
        return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}

class GraphDrawer:
    def DictoinaryToPair(self, dic):
        dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
        categorys = []
        counts = []
        for i in dic:
            categorys.append(i)
            counts.append(dic[i])
        return (categorys, counts)

    def ShowDetailGraphs(self, dict):
        length = len(dict)
        ySize = round(math.sqrt(length))
        xSize = math.ceil(math.sqrt(length))
        fig, axs = plt.subplots(ySize, xSize, figsize=(15,15), squeeze=False)

        currentX = 0
        currentY = 0
        for main in dict:
            self.DrawBar(dict[main], axs[currentY, currentX], main)

            if(currentX < xSize-1):
                currentX += 1
            else:
                currentX = 0
                currentY += 1

        plt.subplots_adjust(bottom=0.15, wspace=0.7, hspace=0.7)
        plt.show()

    def ShowRegionGraphs(self, regions, columnName, type = 'bar'):
        current = 0
        length = len(regions)
        ySize = round(math.sqrt(length))
        xSize = math.ceil(math.sqrt(length))
        fig, axs = plt.subplots(ySize, xSize, figsize=(40,40), squeeze=False)

        for i in axs:
            for graph in i:
                if(len(regions) > current):
                    if(type == 'bar'):
                        self.DrawBar(regions[current].GetCategoryByCount(columnName), graph, regions[current].regionName)
                    elif(type == 'pie'):
                        self.DrawPie(regions[current].GetCategoryByCount(columnName), graph, regions[current].regionName)
                    current += 1
                else:
                    break 

        plt.subplots_adjust(bottom=0.15, wspace=0.7, hspace=0.7)
        plt.show()

    def DrawBar(self, dict, ax, title):
        pair = self.DictoinaryToPair(dict)
        ax.bar(pair[0], pair[1])
        ax.set_title(title)
        ax.tick_params(labelrotation=70)

    def DrawPie(self, dict, ax, title):
        pair = self.DictoinaryToPair(dict)
        ax.set_title(title)
        ax.pie(pair[1], labels=pair[0], autopct='%.1f%%')

keyWord = '제주'
regions = []
for i in os.listdir():
    if(keyWord in i):
        regions.append(Region(i))

# GraphDrawer().ShowRegionGraphs(regions, '상권업종대분류명')

GraphDrawer().ShowDetailGraphs(regions[0].GetCategoryDict('시군구명', '상권업종대분류명'))
# GraphDrawer().ShowDetailGraphs(regions[0].GetCategoryDict_HasFilt(['상권업종대분류명', '음식'], '상권업종대분류명', '상권업종소분류명'))