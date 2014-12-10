#!/usr/bin/python 
#encoding:utf-8

def clustering(clist):
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
        data_dict = {}
        data = self.loaddata(filename = self.normindatafilename)
        print "读取数据中..."
        counter = 0
        for line in data:
            counter += 1
            if counter%1000 == 0:
                print "读入数据 ",counter," 条"
            if line != "" and (not data_dict.has_key(line[0])) :
                tmp = set()
                tmp.add(line[1])
                data_dict[line[0]] = tmp
            elif line != "":
                data_dict[line[0]].add(line[1])
        print "共读入指标数据 ",counter," 条"
        #
        #
        #for k,v in data_dict.iteritems():
        #    print "dict[%s] = " %k,v
        
        for indicator,indi_meta in data_dict.iteritems():
            if len(indi_meta) <= 1:
                print 
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
                        if not year_area_dict.has_key(year+"|"+areacode):
                            year_area_dict[year+"|"+areacode] = [[num,unit,yearbook]]
                        else:
                            year_area_dict[year+"|"+areacode].append([num,unit,yearbook])
            #完成对当前指标建立词典信息 
            
            #遍历当前指标对应的 年份_地区-数值 单位 年鉴 词典
            for year_area,year_area_meta in year_area_dict.iteritems():
                #如果只对应一条数据，则输出
                if len(year_area_meta) == 1:
                    print 
                    continue
                else:
                    norm_num = ""
                    norm_unit = ""
                    norm_yearbook = ""
                    num_list  = []
                    unit_list = []
                    yearbook_list = []
                    for yam_item in year_area_meta:
                        #查找是否有国家级统计年鉴的数据，如果有则直接采用
                        if yam_item[2].find("中国") != -1:
                            norm_num = yam_item[0]
                            norm_unit = yam_item[1]
                            norm_yearbook = yam_item[2]
                            print indicator,year_area,norm_num,norm_unit,norm_yearbook
                            break;
                        else:
                            num_list.append(yam_item[0])
                            unit_list.append(yam_item[1])
                            yearbook_list.append(yam_item[2])
                    #数值和单位分别聚类,寻找最佳值
                    norm_num  = clustering(num_list)
                    norm_unit = clustering(unit_list)
                    #查找最佳数据输出
                    for yam_item in year_area_meta:
                        if yam_item[0] == norm_num and yam_item[1] == norm_unit:
                            norm_yearbook = yam_item[2]
                            break
                        else:
                            #修正单位或数值
                            pass
                    print indicator,year_area,norm_num,norm_unit,norm_yearbook
                
                
                
                
        
    def go(self):
        """
        
        """
        #self.instr_index()
        self.cleaning()
        

if __name__ == "__main__":
    sdc = StatisticalDataCleaning()
    sdc.go()
    print "End!"
    
    
    
    