set number
set mouse=a
set numberwidth=1
set clipboard=unnamed
syntax enable
set showcmd
set ruler
set encoding=utf-8
set showmatch
set sw=4
set relativenumber

set laststatus=2
set noshowmode

call plug#begin('~/.vim/plugged')

" Temas
"Plug 'dracula/vim',{'as':'dracula'}
"Plug 'gosukiwi/vim-atom-dark'
" Plug 'rakr/vim-one'
Plug 'morhetz/gruvbox'

" IDE
Plug 'easymotion/vim-easymotion'
Plug 'scrooloose/nerdtree'
Plug 'christoomey/vim-tmux-navigator'

call plug#end()

colorscheme gruvbox
let g:gruvbox_contrast_dark = "hard"
"colorscheme dracula
"colorscheme atom-dark
"let g:airline_theme='one'

let mapleader = " "

" Atajos
nmap <Leader>s <Plug>(easymotion-s2)
nmap <Leader>nt :NERDTreeFind<CR>
nmap <Leader>w :w<CR>
nmap <Leader>q :q<CR>
nmap <Leader>wq :wq<CR>

imap jj <Esc>

