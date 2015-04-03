; =========================================================================
; Local modifications  ********** OMN 1996 **********

; line-number-mode
(setq line-number-mode t)
(setq column-number-mode t)
(setq meta-flag t)          ; virker ikke
 
; Setup abbreviations
(setq-default abbrev-mode t)
(read-abbrev-file "~/.abbrev_defs")
(setq save-abbrevs t)

; Font lock mode
(global-font-lock-mode t)
(setq font-lock-maximum-decoration t)    

; Disable splash screen
(setq inhibit-splash-screen t)

; Automatically remove superfluous spaces at the end of each line
(add-hook 'before-save-hook 'delete-trailing-whitespace)

; Automatically replace any tabs with spaces (DOES NOT WORK)
;(add-hook 'before-save-hook 'untabify)


; ---------------------------------------------------------------------------
; Define new functions
;
(defun my-newline-and-indent ()
  "newline with same indent as previous nonblank line (OMN-1994)"
  (interactive)
  (newline)
  (indent-relative-maybe)
  )
;;
; Redefinition of Return and line feed
; \C-m is Return
; \C-j is Line Feed
(global-set-key "\C-m" 'my-newline-and-indent)         ; Ret
(global-set-key "\C-j" 'newline)                       ; Line Feed

(defun delete-whitespace ()
  "delete whitespace from point to next character (OMN-1996)"
  (interactive)
  (if (looking-at "\\( \\|\t\\|\n\\)+")
  (delete-region (match-beginning 0) (match-end 0)))
  )
(define-key esc-map "d" 'delete-whitespace)

; ---------------------------------------------------------------------------
; Define keyboard

; Alternative "goto line number"
(global-set-key "\C-x\C-j" 'goto-line)            

; PC style delete & backspace etc
(global-set-key "\C-h" 'backward-delete-char-untabify) ; Backspace
(global-set-key [delete] 'delete-char)                 ; Del
(global-set-key [C-backspace] 'kill-word)              ; Ctrl backspace
(global-set-key [C-left] 'backward-word)               ; Ctrl left arrow
(global-set-key [C-right] 'forward-word)               ; Ctrl right arrow
(global-set-key [home] 'beginning-of-line)             ; PC-home
(global-set-key [end] 'end-of-line)                    ; PC-end
(global-set-key [C-home] 'beginning-of-buffer)         ;
(global-set-key [C-end] 'end-of-buffer)                ;

; other definitions
(global-set-key [C-delete] 'delete-whitespace)         ;
(global-set-key [print] 'kill-line)                    ; Cut
(global-set-key [key-20] 'yank)                        ; Paste
(global-set-key [pause] 'beginning-of-buffer)          ; Go to top
;(global-set-key [key-21] 'keyboard-quit)               ; S-print
(global-set-key [break] 'recenter)                     ; S-pause

;Function keys
(global-set-key [f1] 'help-for-help)                   ; F1
(global-set-key [f2] 'save-buffer)                     ; F2
(global-set-key [f3] 'find-file)                       ; F3
(global-set-key [f4] 'switch-to-buffer)                ; F4
(global-set-key [f5] 'goto-line)                       ; F5
(global-set-key [f6] 'isearch-forward)                 ; F6
(global-set-key [f7] 'query-replace-regexp)            ; F7 - S & R (query)
(global-set-key [f8] 'replace-string)                  ; F8 - Replace
(global-set-key [f9] 'enlarge-window)                  ; F9
(global-set-key [f10] 'save-buffers-kill-emacs)        ; F10
(global-set-key [f11] 'repeat-complex-command)         ; F11
(global-set-key [f12] 'describe-key)                   ; F12

(global-set-key [S-f3] 'insert-file)                   ; S-F3
(global-set-key [kp-f1] 'shrink-window)                ; S-F9
(global-set-key [kp-f4] 'describe-function)            ; S-F12

(put 'downcase-region 'disabled nil)

(put 'upcase-region 'disabled nil)
