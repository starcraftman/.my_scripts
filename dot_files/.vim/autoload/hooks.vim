" Hooks to be used with plug.vim for bundles.
function! hooks#YCMInstall(info)
  if a:info.status == 'installed' || a:info.force
    !./install.sh --clang-completer
  endif
endfunction
