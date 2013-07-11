#coding:utf-8
import string


#判断该字符是否是中文字符（不包括中文标点）    
def isChineseChar(charater):  
    return 0x4e00 <= ord(charater) < 0x9fa6  

#判断是否是ASCII码  
def isASCIIChar(ch):  
    if ch in string.whitespace:  
        return False  
    if ch in string.punctuation:  
        return False  
    return ch in string.printable  
