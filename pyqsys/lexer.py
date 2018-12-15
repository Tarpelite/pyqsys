from C0_lexer import C0lexer
class simple_tkinter_lexer(C0lexer):
    def __init__(self, source_text:str):
        self.SOURCE_TEXT = source_text
        self.p = 0
        self.KEYWORDS = ["proc"]
        self.TOKEN = ""
        self.RESULT = []
        self.REPLY = ""
        self.line_cnt = 0;
        self.word_cnt = 0;
        self.error_message_box =[];
        self.web_word_analyze()
        self.fill_map()
    
    def _retract(self):
        '''
          回退一个字符
        '''
        if self.p > 0 :
            self.p -= 1
        if len(self.TOKEN) > 0:
            self.TOKEN = self.TOKEN[:-1]

    def _isNewLine(self):
        '''
          判断是否是一个新的行
        '''
        if self.curChar() == '\n':
            return True
        return False
    
    def isSharp(self):
        if self.curChar() == "#":
            return True
        return False
    
    def isLetter(self):
        ch = self.curChar()
        if ch!="#" and (not self._isNewLine()) and ch != "{" and ch != "}" and ch!= " ":
            return True
        return False;
    
    def getsym(self):
        self.clearToken()
        lim = len(self.SOURCE_TEXT)
        if self.p >= lim:
            return False
        while self.isSpace() or self.isTab() or self._isNewLine():
            if self._isNewLine():
                self.line_cnt += 1
                self.word_cnt = 0
            self.p += 1
            self.clearToken()
            if self.p >= lim:
                return False
        res = [self.line_cnt, self.word_cnt]
        if self.isLetter():
            while self.isLetter() or self.isDigit():
                self.getchar()
            if self.isKeyWord():
                res.extend(['关键字', self.TOKEN.upper()])
            else:
                res.extend(['标识符', self.TOKEN])
        elif self.isDigit():
            if self.TOKEN == '0':
                res.extend(['整数', self.TOKEN])
            else:
                while self.isDigit():
                    self.getchar()
                res.extend(['整数', self.TOKEN])
        elif self.isMinus():
            flag = 0
            self.getchar()
            while self.isDigit():
                if flag == 0:
                    flag = 1
                self.getchar()
            if flag == 0:
                res.extend(['-', '-'])
            else:
                res.extend(['整数', int(self.TOKEN)])
        elif self.isPlus():
            flag = 0
            self.getchar()
            while self.isDigit():
                if flag == 0:
                    flag = 1
                self.getchar()
            if flag == 0:
                res.extend(['+',  '+'])
            else:
                res.extend(['整数', int(self.TOKEN)])
        elif self.isQuote():
            flag = 0
            self.p += 1
            while not self.isQuote():
                if self.isInvalidchar():
                    self.p += 1
                    if self.p >= len(self.SOURCE_TEXT):
                        return False
                elif self.isTrans():
                    self.p += 1
                    if self.p >= len(self.SOURCE_TEXT):
                        return False
                    self.getchar()
                else:
                    self.getchar()
            self.p += 1
            res.extend(['字符串', self.TOKEN])
        elif self.isLess():
            self.getchar()
            if self.isEqu():
                self.getchar()
                res.extend(["关系运算符", "<="])
            else:
                res.extend(["关系运算符", "<"])
        elif self.isMore():
            self.getchar()
            if self.isEqu():
                self.getchar()
                res.extend(["关系运算符", ">="])
            else:
                res.extend(["关系运算符", ">"])
        elif self.isMark():
            self.getchar()
            if self.isEqu():
                self.getchar()
                res.extend(['关系运算符', '!='])
            else:
                self._error()
        elif self.isEqu():
            self.getchar()
            if self.isEqu():
                self.getchar()
                res.extend(["关系运算符", "=="])
            else:
                res.extend(['专用符号', "="])
        elif self.isMult():
            self.getchar()
            res.extend(['*', '*'])
        elif self.isDiv():
            self.getchar()
            res.extend(['/', '/'])
        elif self.isLpar():
            self.getchar()
            res.extend(['专用符号', '('])
        elif self.isRpar():
            self.getchar()
            res.extend(['专用符号', ')'])
        elif self.isBigLpar():
            self.getchar()
            res.extend(['专用符号', '{'])
        elif self.isBigRpar():
            self.getchar()
            res.extend(['专用符号', '}'])
        elif self.isComma():
            self.getchar()
            res.extend(['专用符号', ','])
        elif self.isSemi():
            self.getchar()
            res.extend(['专用符号', ';'])
        elif self.isSharp():
            self.getchar()
            res.extend(['专用符号', "#"])
        else:
            self._error()
        self.word_cnt += 1
        self.RESULT.append(res)
        if len(res) < 3:
            return False
        self.REPLY += "[" + str(res[2]) + ", " + str(res[3]) + "]\n"
       # print(res)
        return True
    
    def _error(self):
        '''
            增加报错信息
        '''
        msg = "词法错误：第" + str(self.line_cnt) + "行,第" + str(self.word_cnt) + "个单词：" + str(self.TOKEN)
        self.error_message_box.append(msg)
    
    def print_result(self):
        '''
            打印结果
        '''

        for res in self.RESULT:
            print("行：" + str(res[0]) + " 个: " + str(res[1]) + " 类型: " + str(res[2]) + " 值: " + str(res[3]))
        #print(self.error_report())
    
    def get_words(self):
        self.words = self.RESULT
        self.words_p = 0
        self.map = []
        for i in range(self.line_cnt):
            self.map.append(False)
    
    def _getword(self):
        '''
            返回下一个单词
        '''
        if self.words_p < len(self.words) and self.words_p >= 0:
            res = self.words[self.words_p]
            self.words_p += 1
            return res
        return False

    def _curword(self):
        '''
            返回当前指针所指的单词
        '''
        if self.words_p < len(self.words) and self.words_p >= 0:
            return self.words[self.words_p]
        return False
    
    def s_proc(self):
        '''
            <proc语句> -> proc '<标识符>' '{'<语句序列>'}''{'<语句序列>'}'
        '''
        self._getword()
        wd = self._curword()
        start = wd[0]
        if wd[2] != '标识符':
            return False
        self._getword()
        wd = self._curword()
        if wd[2] != '专用符号' or wd[3] != '{':
            return False
        self._getword()
        self.s_statement_series()
        wd = self._curword()
        if wd[2] != '专用符号' or wd[3] != '}':
            return False
        self._getword()
        wd = self._curword()
        if wd[2] != '专用符号' or wd[3] != '{':
            return False
        self._getword()
        self.s_statement_series()
        wd = self._curword()
        if wd[2] != '专用符号' or wd[3] != '}':
            return False
        wd = self._getword()
        end = wd[0]
        for i in range(start, end+1):
            self.map[i] = True
        return True
    
    def s_statement_series(self):
        '''
            ＜语句序列＞ ::=  ＜语句＞｛＜语句＞｝ 

        '''
        res = self.s_statement()
        if not res:
            return False
        wd = self._curword()
        while (wd[2] == '标识符' or (wd[2] == '专用符号' and wd[3] == '{')) :
            res = self.s_statement()
            if res:
                wd = self._curword()
            else:
                break
        return True
    
    def s_statement(self):
        '''
        ＜语句＞ ::= ‘{’<语句序列>‘}’｜＜空＞ | {标识符}
        '''
        wd = self._curword()
        if wd[2] == '专用符号' and wd[3] == '{':
            self._getword()
            res = self.s_statement_series()
            if not res:
                return False
            wd = self._curword()
            if wd[2] != '专用符号' or wd[3] != '}':
                self._error("应为}")
                return False
            self._getword()
        elif wd[2] == '标识符':
            while wd[2] == "标识符":
                self._getword()
                wd = self._curword()
        return True
        
    
    
    def fill_map(self):
        self.get_words()
        while self.words_p < len(self.words):
            wd = self._curword()
            if wd[2] == '关键字' and wd[3] == 'PROC':
                self.s_proc()
                continue
            self._getword()
    
    def judge_line(self, i):
        return self.map[i]
            
            



if __name__ == "__main__":
    with open("/home/tarpe/shared/Fix_Length_Bytes2Packets_hw.tcl") as f:
        txt = f.read()
    lexer = simple_tkinter_lexer(txt)
    #lexer.print_result()
    print(lexer.judge_line(146))

