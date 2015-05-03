import sublime, sublime_plugin
import random, re

root = "/Users/snuke/Documents/library/"

def genRand(l,r):
  return str(random.randint(l,r-1))

class LibraryPasteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # template
    if self.view.size() == 0:
      self.paste(edit, self.view.line(0), "template")
    # library
    sels = self.view.find_all(r"^\[.*?\]")
    for sel in sels[::-1]:
      self.paste(edit, sel, self.view.substr(sel)[1:-1])
    # [rand]
    sels = self.view.find_all(r"\[rand\]")
    for sel in sels[::-1]:
      self.view.replace(edit, sel, genRand(10**5,10**6))
    sels = self.view.find_all(r"\[\d*\}")
    for sel in sels[::-1]:
      s = self.view.substr(sel)[1:-1]
      l = 10**5
      r = 10**6
      if s != "":
        l = 0
        r = int(s) 
      self.view.replace(edit, sel, genRand(l,r))
    # scanf
    sels = self.view.find_all(r"scn [\w,\-\[\]]*")
    for sel in sels[::-1]:
      clauses = re.split(r" |,", self.view.substr(sel))[1:]
      format = ""
      args = ""
      for clause in clauses:
        parts = clause.split("-")
        if len(parts) == 1: parts.append("d")
        if parts[1] == "l": parts[1] = "lld"
        if parts[1] != "s": parts[0] = "&" + parts[0]
        if parts[1] == "c": format += " "
        format += "%" + parts[1]
        args += "," + parts[0]
      result = "scanf(\"%s\"%s)" % (format, args)
      print self.view.substr(sel)
      print self.view.line(sel).end(),sel.end()
      if self.view.line(sel).end() == sel.end(): result += ';'
      self.view.replace(edit, sel, result)
    # couts
    sels = self.view.find_all(r"cout,[^;]*;")
    for sel in sels[::-1]:
      s = self.view.substr(sel)[5:]

      if s[-1] == ';': s = s[:-1]
      nest = 0
      result = "cout<<"
      for c in s:
        if c == '(' or c == '{': nest += 1
        if c == ')' or c == '}': nest -= 1
        if c == ',' and nest == 0: result += "<<\" \"<<"
        else: result += c
      result += "<<endl;"
      self.view.replace(edit, sel, result)

  # paste library
  def paste(self, edit, sel, name):
    try:
      f = open(root+name+".cpp", "r")
      self.view.replace(edit, sel, f.read())
      f.close()
    except: pass
