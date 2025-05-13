let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Programs/fantasy
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +564 yfpy_nhl_sqlite/queries.py
badd +49 yfpy_nhl_sqlite/main.py
badd +7 .env
badd +130 venv/lib/python3.13/site-packages/yfpy/query.py
badd +16 pyproject.toml
badd +21 scratch.sql
badd +1 README.md
badd +26 yfpy_nhl_sqlite/schema.sql
badd +119 LICENSE
badd +1 /private/var/folders/08/qp50tv454_97022ypy853rjr0000gn/T/nvim.jesse.kearl/FapxqH/16.dbout
badd +1 venv/lib/python3.13/site-packages/yfpy/__init__.py
badd +2 .gitignore
badd +47 scratch.py
badd +1 /private/var/folders/08/qp50tv454_97022ypy853rjr0000gn/T/nvim.jesse.kearl/OL6mBj/11.dbout
argglobal
%argdel
edit README.md
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 135 + 119) / 238)
exe '2resize ' . ((&lines * 36 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 102 + 119) / 238)
exe '3resize ' . ((&lines * 12 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 102 + 119) / 238)
argglobal
balt yfpy_nhl_sqlite/main.py
setlocal foldmethod=indent
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=100
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 30 - ((29 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 30
normal! 014|
lcd ~/Programs/fantasy
wincmd w
argglobal
if bufexists(fnamemodify("~/Programs/fantasy/scratch.sql", ":p")) | buffer ~/Programs/fantasy/scratch.sql | else | edit ~/Programs/fantasy/scratch.sql | endif
if &buftype ==# 'terminal'
  silent file ~/Programs/fantasy/scratch.sql
endif
balt ~/Programs/fantasy/yfpy_nhl_sqlite/schema.sql
setlocal foldmethod=indent
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=100
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 27 - ((17 * winheight(0) + 18) / 36)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 27
normal! 0
lcd ~/Programs/fantasy
wincmd w
argglobal
if bufexists(fnamemodify("~/Programs/fantasy/scratch.py", ":p")) | buffer ~/Programs/fantasy/scratch.py | else | edit ~/Programs/fantasy/scratch.py | endif
if &buftype ==# 'terminal'
  silent file ~/Programs/fantasy/scratch.py
endif
balt ~/Programs/fantasy/yfpy_nhl_sqlite/queries.py
setlocal foldmethod=indent
setlocal foldexpr=0
setlocal foldmarker={{{,}}}
setlocal foldignore=#
setlocal foldlevel=100
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldenable
let s:l = 41 - ((8 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 41
normal! 050|
lcd ~/Programs/fantasy
wincmd w
exe 'vert 1resize ' . ((&columns * 135 + 119) / 238)
exe '2resize ' . ((&lines * 36 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 102 + 119) / 238)
exe '3resize ' . ((&lines * 12 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 102 + 119) / 238)
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
let g:this_session = v:this_session
let g:this_obsession = v:this_session
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
