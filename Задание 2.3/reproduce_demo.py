"""Reproducible Git exercise. Creates a new temporary folder; never edits a user's repo."""
from pathlib import Path
import subprocess, tempfile, shutil, json, os, sys, time

root = Path(tempfile.mkdtemp(prefix='practice-git-'))
repo, remote, clone = root/'student', root/'origin.git', root/'review'
repo.mkdir()
records=[]
env=os.environ.copy()
env.update(GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
def git(cwd,*args,expected=0):
    cmd=['git','-c','core.autocrlf=false','-c','core.quotepath=false',*args]
    r=subprocess.run(cmd,cwd=cwd,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True)
    out=(r.stdout+r.stderr).replace(str(root),'<DEMO>').replace(root.as_posix(),'<DEMO>')
    records.append({'cwd':Path(cwd).name,'command':'git '+' '.join(args),'exit':r.returncode,'output':out.rstrip()})
    if r.returncode != expected: raise RuntimeError(records[-1])
    return r.stdout.strip()
def write(cwd,name,content):
    (cwd/name).write_text(content,encoding='utf-8',newline='\n')
    records.append({'cwd':cwd.name,'command':f'WRITE {name}','exit':0,'output':content.rstrip()})
def identity(cwd):
    git(cwd,'config','user.name','Качков Кирилл Евгеньевич')
    git(cwd,'config','user.email','student@example.invalid')
git(root,'--version')
git(repo,'init','-b','main'); identity(repo)
write(repo,'README.md','# Practice Git demo\n')
write(repo,'plan.txt','review=draft\n')
write(repo,'.gitignore','*.tmp\n')
write(repo,'scratch.tmp','ignored local notes\n')
git(repo,'status','--short')
git(repo,'add','README.md','plan.txt','.gitignore')
git(repo,'diff','--cached','--stat')
git(repo,'commit','-m','Add initial practice plan')
git(repo,'switch','-c','feature/report')
write(repo,'plan.txt','review=feature-version\n')
git(repo,'diff');git(repo,'add','plan.txt');git(repo,'commit','-m','Prepare report in feature branch')
git(repo,'switch','main')
write(repo,'plan.txt','review=main-version\n')
git(repo,'add','plan.txt');git(repo,'commit','-m','Update main review plan')
git(repo,'merge','feature/report',expected=1)
git(repo,'status','--short');git(repo,'diff','--','plan.txt')
write(repo,'plan.txt','review=checked-and-ready\n')
git(repo,'add','plan.txt');git(repo,'commit','-m','Resolve review plan conflict')
write(repo,'plan.txt','review=temporary-draft\n')
git(repo,'diff');git(repo,'restore','plan.txt')
git(repo,'status','--short')
write(repo,'README.md','# Practice Git demo\nUnneeded experimental note.\n')
git(repo,'add','README.md');git(repo,'commit','-m','Add experimental note')
git(repo,'revert','--no-edit','HEAD')
git(root,'init','--bare','--initial-branch=main','origin.git')
git(repo,'remote','add','origin','../origin.git')
git(repo,'push','-u','origin','main')
git(root,'clone','origin.git','review');identity(clone)
write(clone,'review.txt','Reviewed in second working copy.\n')
git(clone,'add','review.txt');git(clone,'commit','-m','Add review result');git(clone,'push')
git(repo,'fetch','origin');git(repo,'log','--oneline','HEAD..origin/main');git(repo,'pull','--ff-only')
git(repo,'tag','v1.0')
git(repo,'log','--graph','--oneline','--all','--decorate')
git(repo,'status')
assert git(repo,'status','--porcelain') == ''
assert (repo/'plan.txt').read_text()=='review=checked-and-ready\n'
assert (repo/'README.md').read_text()=='# Practice Git demo\n'
assert (repo/'review.txt').is_file()
out=root/'evidence'
out.mkdir(exist_ok=True)
git(repo,'bundle','create',str(out/'practice-history.bundle'),'--all')
(out/'commands.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'terminal-session.txt').write_text('\n\n'.join(f"[{x['cwd']}] $ {x['command']}\n{x['output']}\n[exit {x['exit']}]" for x in records),encoding='utf-8')
print(json.dumps({'commands':len(records),'version':records[0]['output'],'result':'PASS','evidence':str(out)},ensure_ascii=False))
