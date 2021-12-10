import sublime, sublime_plugin
import random, re, os

# root directory
root = ''
root_path = os.path.join(os.path.dirname(__file__), 'root.txt')
with open(root_path) as f:
  root = f.readline()

def genRand(l,r):
  return str(random.randint(l,r-1))

class LibraryPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # template
    if self.view.size() == 0:
      self.paste(edit, self.view.line(0), 'template')

    # library
    sels = self.view.find_all(r'^\[.*?\]')
    for sel in sels[::-1]:
      self.paste(edit, sel, self.view.substr(sel)[1:-1])

    # [rand]
    sels = self.view.find_all(r'\[rand\]')
    for sel in sels[::-1]:
      self.view.replace(edit, sel, genRand(10**5,10**6))
    sels = self.view.find_all(r'\[\d*\}')
    for sel in sels[::-1]:
      s = self.view.substr(sel)[1:-1]
      l = 10**5
      r = 10**6
      if s != '':
        l = 0
        r = int(s) 
      self.view.replace(edit, sel, genRand(l,r))

    # df
    sels = self.view.find_all(r'df [\w,:\.]*')
    for sel in sels[::-1]:
      clauses = re.split(r' |,', self.view.substr(sel))[1:]
      format = ''
      args = ''
      df = {}
      for clause in clauses:
        parts = clause.split(':')
        if len(parts) == 1: parts.append('d')
        typ = 'int'
        if parts[1] == 'l': typ = 'll'
        if parts[1] == 'f': typ = 'double'
        if parts[1] == 'c': typ = 'char'
        if parts[1] == 's': typ = 'str'
        if typ not in df: df[typ] = []
        df[typ].append(parts[0])
        if parts[1] == 'l': parts[1] = 'lld'
        if parts[1] == 'f': parts[1] = 'lf'
        if parts[1] != 's': parts[0] = '&' + parts[0]
        if parts[1] == 'c': format += ' '
        format += '%' + parts[1]
        args += ',' + parts[0]
      result = ''
      nl = ';\n' + ' '*self.view.rowcol(sel.a)[1]
      for typ,vs in df.items():
        if typ == 'str': continue
        result += typ + ' ' + ','.join(vs) + nl
      result += 'scanf("%s"%s)' % (format, args)
      if self.view.line(sel).end() == sel.end(): result += ';'
      self.view.replace(edit, sel, result)

    # scanf
    sels = self.view.find_all(r'scn ([\w,:\.]|\[[^\s,:]*\])*')
    for sel in sels[::-1]:
      clauses = re.split(r' |,', self.view.substr(sel))[1:]
      format = ''
      args = ''
      for clause in clauses:
        parts = clause.split(':')
        if len(parts) == 1: parts.append('d')
        if parts[1] == 'l': parts[1] = 'lld'
        if parts[1] == 'f': parts[1] = 'lf'
        if parts[1] != 's': parts[0] = '&' + parts[0]
        if parts[1] == 'c': format += ' '
        format += '%' + parts[1]
        args += ',' + parts[0]
      result = 'scanf("%s"%s)' % (format, args)
      if self.view.line(sel).end() == sel.end(): result += ';'
      self.view.replace(edit, sel, result)

    # struct
    sels = self.view.find_all(r'^st [\w,:\.]*')
    for sel in sels[::-1]:
      clauses = re.split(r' |,', self.view.substr(sel))[1:]
      # typs = ['int','ll','double','char','string']
      name,clauses = clauses[0],clauses[1:]
      varList,pretyp = [],''
      for clause in clauses:
        parts = clause.split(':')
        if len(parts) == 1: parts.append('d')
        typ = 'int'
        if parts[1] == 'l': typ = 'll'
        if parts[1] == 'f': typ = 'double'
        if parts[1] == 'c': typ = 'char'
        if parts[1] == 's': typ = 'string'
        if pretyp != typ:
          pretyp = typ
          varList.append([typ])
        varList[-1].append(parts[0])
      lines = []
      args = []
      for vs in varList:
        typ,vs = vs[0],vs[1:]
        lines.append(typ + ' ' + ', '.join(vs) + ';')
        zero = '0'
        if typ == 'string':
          zero = '""'
        for val in vs:
          args.append([val,typ,zero])
      con = name+'('
      for arg in args:
        con += arg[1]+' '+arg[0]+'='+arg[2]+', '
      con = con[:-2]+'):'
      for arg in args:
        con += arg[0]+'('+arg[0]+'),'
      con = con[:-1]+' {}'
      lines.append(con)

      con = 'bool operator<(const '+name+'& _) const { return '
      con += args[0][0]+'<_.'+args[0][0]+';}'
      lines.append(con)

      result = 'struct '+name+' {\n'
      for line in lines:
        result += '  '+line+'\n'
      result += '};\n'

      result += 'istream& operator>>(istream&i,'+name+'&a){return i'
      for arg in args:
        result += '>>a.'+arg[0]
      result += ';}\nostream& operator<<(ostream&o,const '+name+'&a){return o'
      result += '<<" "'.join(['<<a.'+arg[0] for arg in args])
      result += ';}'

      self.view.replace(edit, sel, result)

    # cin,cout,cerr
    sels = self.view.find_all(r'c(err|in|out),[^;]*?(;|$)')
    for sel in sels[::-1]:
      s = self.view.substr(sel)
      cs,op = s[:4],'<<'
      if cs[1] == 'i':
        cs,op = cs[:-1],'>>'
      s = s[len(cs)+1:]

      if s[-1] == ';': s = s[:-1]
      nest = 0
      quote = 0
      result = cs + op
      for c in s:
        if quote == 0:
          if c == '"': quote = 1
          if c == '(' or c == '{': nest += 1
          if c == ')' or c == '}': nest -= 1
          if c == ',' and nest == 0:
            if cs == 'cin':
              result += '>>'
            else:
              result += '<<" "<<'
          else: result += c
        else:
          if c == '"': quote = 0
          result += c
      if cs == 'cin':
        result += ';'
      else:
        result += '<<endl;'
      self.view.replace(edit, sel, result)

    # print
    sels = self.view.find_all(r'print,[^;]*?(;|$)')
    for sel in sels[::-1]:
      s = self.view.substr(sel)[6:]
      if s[-1] == ';': s = s[:-1]
      mode = 0
      nest = 0
      result = 'printf("'
      for c in s:
        if mode == 0:
          if c == ',':
            mode = 1
            result = result[:-1] + '\\n",'
          else:
            format = c
            if c == 'l': format = 'lld'
            if c == 'f': format = '.10f'
            result += '%' + format
            result += ' '
        else: result += c
      result += ');'
      self.view.replace(edit, sel, result)

    # to[a].pb(b);g -> to[b].pb(a);
    sels = self.view.find_all(r'^.*;g$')
    for sel in sels[::-1]:
      s = self.view.substr(sel)[:-1]
      s = re.sub(r'\[a\]', '[DaMmY]', s)
      s = re.sub(r'\(a\)', '(DaMmY)', s)
      s = re.sub(r'\(a,', '(DaMmY,', s)
      s = re.sub(r'\[b\]', '[a]', s)
      s = re.sub(r'\(b\)', '(a)', s)
      s = re.sub(r'\(b,', '(a,', s)
      s = re.sub('DaMmY', 'b', s)
      self.view.replace(edit, sel, s)

    # rin -> rep(i,n)
    for region in self.view.sel():
      line = self.view.line(region)
      s = self.view.substr(line)
      s = re.sub(r'r(\w)(\w*)$', r'rep(\1,\2)', s)
      self.view.replace(edit, line, s)

    # init
    sels = self.view.find_all(r'init,[^;]*?(;|$)')
    for sel in sels[::-1]:
      s = self.view.substr(sel)[5:]
      if s[-1] == ';': s = s[:-1]
      s = s.split(',')
      d,s,x = s[0],s[1:-1],s[-1]
      result = ''
      for i in range(len(s)):
        result += 'rep(i{0},{1}+1)'.format(i,s[i])
      result += ' '+d
      for i in range(len(s)):
        result += '[i{0}]'.format(i)
      result += ' = '+x+';'
      self.view.replace(edit, sel, result)

  # paste library
  def paste(self, edit, sel, name):
    try:
      f = open(root+name+'.cpp', 'r')
      self.view.replace(edit, sel, f.read())
      f.close()
    except:
      try:
        f = open(root+'macro/'+name+'.cpp', 'r')
        self.view.replace(edit, sel, f.read())
        f.close()
      except: pass

class InsertMacroCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel('Input macro name:','',self.on_done,None,None)
  def on_done(self,name):
    self.window.run_command('paste_macro',{'name':name})

class PasteMacroCommand(sublime_plugin.TextCommand):
  def run(self,edit,name):
    self.paste(edit,name)
  # paste library
  def paste(self,edit,name):
    try:
      if name[-1] == ';':
        with open(root+name[:-1]+'.cpp', 'r') as f:
          sel = self.view.sel()[0]
          nl = '\n' + ' '*self.view.rowcol(sel.a)[1]
          self.view.insert(edit, sel.a, f.read().replace('\n', nl))
      else:
        with open(root+name+'.cpp', 'r') as f:
          pos = self.view.find(r'^$', 0)
          self.view.insert(edit, pos.a, '\n'+f.read())
    except:
      try:
        with open(root+'macro/'+name+'.cpp', 'r') as f:
          pos = self.view.find(r'^$', 0)
          self.view.insert(edit, pos.a, f.read()+'\n')
      except: pass
