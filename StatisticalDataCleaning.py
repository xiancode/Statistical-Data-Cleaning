#!/usr/bin/python 
#encoding:utf-8

class StatisticalDataCleaning():
    """
    
    """
    
    infilename = "data.txt"
    dictfilename = "instr_indicator_dict.txt"
    outfilename = "result.txt"
    
    def loaddata(self):
        """
        read data from in file
        """
        result = []
        fin = open(self.infilename,"r")
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
        """
        data = self.loaddata()
        print "load file successed!"
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
        
    def go(self):
        """
        
        """
        self.instr_index()
        

if __name__ == "__main__":
    sdc = StatisticalDataCleaning()
    sdc.go()
    print "End!"
    
    
    
    