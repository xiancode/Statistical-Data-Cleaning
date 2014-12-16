#!/usr/bin/python 
#encoding:utf-8

import string
import copy


def stofdict(slist):
    """
    根据传入的字符串序列，生成与字符串序列相对应的 浮点数 - 字符串 词典
    """
    result = {}
    flist = [string.atof(item) for item in slist]
    for i in range(len(slist)):
        result[flist[i]] = slist[i]
    return result
        
        
def max_num(slist):
    """
    传入数据形字符串，获得数值最大的字符串
    """
    flist = [string.atof(item) for item in slist]
    maxnum = max(flist)
    d = stofdict(slist)
    return d[maxnum]
    
    


def strltofl(strlist):
    """
    字符串序列转化为float序列
    """
    return [string.atof(tmp) for tmp in strlist]

def samelevel(data_list):
    """
    判断序列中的数据是否属于同一数据级别
    """
    #dlist = copy.copy(data_list)
    dlist = strltofl(data_list)
    dlist.sort()
    if dlist[-1]/dlist[0] >= 10:
        return False
    return True
    

def clustering(clist):
    """
    返回高频数值
    """
    cset = set(clist)
    if len(cset) == 1:
        return cset.pop()
    cdict = {}
    for item in clist:
        if not cdict.has_key(item):
            cdict[item] = 1
        else:
            cdict[item] += 1
    values = cdict.values()
    if len(set(values)) == 1:
        return max_num(cdict.keys())
    else:        
        tmp = sorted(cdict.items(),lambda x,y:cmp(x[1],y[1]))
        return  tmp[-1][0]
    
def clustering_unit(clist):
    """
    返回高频单位
    """
    cset = set(clist)
    if len(cset) == 1:
        return cset.pop()
    cdict = {}
    for item in clist:
        if not cdict.has_key(item):
            cdict[item] = 1
        else:
            cdict[item] += 1     
    tmp = sorted(cdict.items(),lambda x,y:cmp(x[1],y[1]))
    return  tmp[-1][0]

def one2one(d):
    """
    判断是否位1对1的映射
    """
    for k,v in d.iteritems():
        if len(v) >=2:
            return False
    
    tmplist = []
    for k,v in d.iteritems():
        for item in v:
            tmplist.append(item)
    s = set(tmplist)
    if len(s) < len(tmplist):
        return False
    else:
        return True
            
    
    s = set(v)
    if len(s) < len(v):
        return False
    else:
        return True
    #for k,v in d.iteritems():
    #    if len(v) >= 2:
    #        return False
    #return True
    

class StatisticalDataCleaning():
    """
    
    """
    
    infilename = "data.txt"
    dictfilename = "instr_indicator_dict.txt"
    outfilename = "result.txt"
    normindatafilename = "normindex_test.txt"
    
    def loaddata(self,filename = infilename):
        """
        read data from in file
        """
        result = []
        fin = open(filename,"r")
        text = fin.readlines();
        for line in text:
            line = line.strip()
            pos = line.find("\t")
            instr = line[:pos]
            instr_last = line[pos+1:]
            tmp = []
            tmp.append(instr)
            tmp.append(instr_last)
            result.append(tmp)
        fin.close()
        return result
    
    def loaddict(self):
        """
        load dict data from in file 
        """
        result = {}
        fin = open(self.dictfilename,"r")
        text = fin.readlines()
        for line in text:
            line = line.strip()
            tmp_list = line.split('\t')
            if len(tmp_list) == 3:
                if not result.has_key(tmp_list[0]):
                    result[tmp_list[0]] = tmp_list[2]
                else:
                    pass
            else:
                pass
        fin.close()
        return result
                    
    
    def instr_index(self):
        """
        Change indicator string to normal indicator 
        指标字符串转化成正式指标
        """
        data = self.loaddata()
        print "load file successed!"
        #载入指标字符串 - 正式指标词典
        dict = self.loaddict()
        print "load dict successed!" 
        result = []
        count = 0
        for item in data:
            count += 1
            if count%1000 == 0:
                print count
            if dict.has_key(item[0]):
                indicator = dict[item[0]]
                result.append(indicator + "\t" + item[1])
            else:
                pass
        
        out_text = ""
        for item in result:
            out_text += item + "\n"
        fout = open(self.outfilename,"w")
        fout.write(out_text)
        fout.close()
        
        
    def cleaning(self):
        """
        数据清洗主程序
        """
        result_str = ""
        #指标与对应信息词典
        data_dict = {}
        data = self.loaddata(filename = self.normindatafilename)
        print "读取数据中..."
        counter = 0
        for line in data:
            counter += 1
            if counter%1000 == 0:
                print "读入数据 ",counter," 条"
            if line != "" and (not data_dict.has_key(line[0])) :
                tmp = []
                tmp.append(line[1])
                data_dict[line[0]] = tmp
            elif line != "":
                data_dict[line[0]].append(line[1])
        print "共读入指标数据 ",counter," 条","需要处理指标 :",len(data_dict)," 个"
        #
        #
        #for k,v in data_dict.iteritems():
        #    print "dict[%s] = " %k,v
        
        counter = 0
        for indicator,indi_meta in data_dict.iteritems():
            counter += 1
            print indicator
            if counter % 500 == 0:
                print "正在处理第 ",counter," 条指标"
            if len(indi_meta) <= 1:
                #print indicator,string.join(indi_meta.pop())
                tmp_meta_str = indi_meta.pop()
                tmp_meta_list = tmp_meta_str.split("\t")
                pstr =  indicator+ "\t" + tmp_meta_list[2] + "\t" + tmp_meta_list[4] + "\t" \
                    + tmp_meta_list[0] + "\t" + tmp_meta_list[1] + "\t" + tmp_meta_list[3]
                #print pstr
                result_str += pstr + "\n"
                continue
            else:
            #以年份和地区代码为key，建立词典
                year_area_dict = {}
                for item in indi_meta:
                    item_list = item.split("\t")        #获取当前指标对应的数一条数值、单位、地区代码、年鉴、年份信息
                    if len(item_list) == 5:
                        [num,unit,areacode,yearbook,year] = item_list
                        # 判断字段是否为空，为空则直接跳过
                        num      = num.strip()
                        unit     = unit.strip()
                        areacode = areacode.strip()
                        yearbook = yearbook.strip()
                        year     = year.strip()
                        if num == "" or unit == "" or areacode == "" or yearbook == "" or year == "":
                            continue
                        if not year_area_dict.has_key(areacode+"\t"+year):
                            year_area_dict[areacode+"\t"+year] = [[num,unit,yearbook]]
                        else:
                            year_area_dict[areacode+"\t"+year].append([num,unit,yearbook])
            #完成对当前指标建立词典信息 
            
            #遍历当前指标对应的 年份_地区-数值 单位 年鉴 词典
            for year_area,year_area_meta in year_area_dict.iteritems():
                #如果只对应一条数据，则输出
                if len(year_area_meta) == 1:
                    pstr =  indicator + "\t" + year_area + "\t" + string.join(year_area_meta[0],"\t")
                    #print pstr
                    result_str += pstr + "\n"
                    continue
                else:
                    norm_num = ""
                    norm_unit = ""
                    norm_yearbook = ""
                    num_list  = []
                    unit_list = []
                    yearbook_list = []
                    cluster_flag = True
                    num_unit_dict = {}
                    unit_num_dict = {}
                    numunit_yearbook_dict = {}
                    for yam_item in year_area_meta:
                        #查找是否有国家级统计年鉴的数据，如果有则直接采用
                        if yam_item[2].find("中国") != -1:
                            norm_num = yam_item[0]
                            norm_unit = yam_item[1]
                            norm_yearbook = yam_item[2]
                            pstr =  indicator + "\t" + year_area + "\t" + norm_num + "\t" + norm_unit + "\t" + norm_yearbook
                            result_str += pstr + "\n"
                            cluster_flag = False
                            break;
                        else:
                            #构建当前 数值对应单位 词典
                            if not num_unit_dict.has_key(yam_item[0]):
                                num_unit_dict[yam_item[0]] = [yam_item[1]]
                            else:
                                num_unit_dict[yam_item[0]].append(yam_item[1])
                            #构建当前 单位对应数值 词典
                            if not unit_num_dict.has_key(yam_item[1]):
                                unit_num_dict[yam_item[1]] = [yam_item[0]]
                            else:
                                unit_num_dict[yam_item[1]].append(yam_item[0])
                            #构建 数值_单位 - 年鉴名称 词典
                            numunit_yearbook_dict[yam_item[0]+"\t"+yam_item[1]] = yam_item[2]
                            num_list.append(yam_item[0])
                            unit_list.append(yam_item[1])
                            yearbook_list.append(yam_item[2])
                    
                    #数值和单位分别聚类,寻找最佳值
                    if cluster_flag == True:
                        #只有一个单位
                        if len(unit_num_dict) == 1:
                            [norm_unit,tmp_nums] = unit_num_dict.popitem()
                            norm_num  = clustering(num_list)
                        #只有一个数值
                        elif len(num_unit_dict) == 1:
                            [norm_num,tmp_units] = num_unit_dict.popitem()
                            norm_unit = clustering_unit(tmp_units)
                        #多个单位和数值
                        elif one2one(num_unit_dict) and one2one(unit_num_dict):
                            if samelevel(num_list):
                                norm_num = max_num(num_list)
                                norm_unit = num_unit_dict[norm_num][0]
                            #norm_yearbook = numunit_yearbook_dict[norm_num + "\t" + norm_unit]
                            else:
                                #修正单位
                                norm_num  = clustering(num_list)
                                norm_unit = clustering_unit(unit_list) 
                                
                        else:
                            norm_num  = clustering(num_list)
                            norm_unit = clustering_unit(unit_list)
                            #查找最佳数据输出
                            for yam_item in year_area_meta:
                                if yam_item[0] == norm_num and yam_item[1] == norm_unit:
                                    norm_yearbook = yam_item[2]
                                    break
                                else:
                                    #修正单位或数值
                                    pass
                        norm_yearbook = numunit_yearbook_dict[norm_num + "\t" + norm_unit]
                        pstr =  indicator + "\t" + year_area + "\t" + norm_num + "\t" +  norm_unit + "\t" + norm_yearbook
                        result_str += pstr + "\n"
        fout = open("Cleaning_Result.txt",'w')
        fout.write(result_str)
        fout.close()        
                
                
                
        
    def go(self):
        """
        
        """
        #self.instr_index()
        self.cleaning()
        

if __name__ == "__main__":
    sdc = StatisticalDataCleaning()
    sdc.go()
    print "End!"
    
    
    
    