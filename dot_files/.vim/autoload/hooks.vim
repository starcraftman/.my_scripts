" Hooks to be used with plug.vim for bundles.
function! hooks#YCMInstall(info)
  if a:info.status == 'installed' || a:info.force
    "execute 'silent !./install.sh --clang-completer &'
    !echo 'hello there'
  endif
endfunction
