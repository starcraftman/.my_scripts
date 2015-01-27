" Hooks to be used with plug.vim for bundles.
function! hooks#YCMInstall(info)
  if a:info.status == 'installed' || a:info == 'updated' || a:info.force
    silent ! ./install.sh --clang-completer >/dev/null 2>&1 &
    redraw!
  endif
endfunction
