(define-abbrev-table 'log-edit-mode-abbrev-table '(
    ("'nn" "\\nonumber" nil 0)
    ("'bcode" "{\\small \\begin{verbatim}" nil 0)
    ("'fr" "\\frac{}{}" nil 0)
    ("'eeqa" "\\end{eqnarray*}" nil 0)
    ("'ev" "\\end{verbatim}" nil 0)
    ("'beqa" "\\begin{eqnarray*}" nil 0)
    ("'et" "\\end{tabular}" nil 0)
    ("'beq" "\\begin{equation}" nil 0)
    ("'es" "\\end{slide}" nil 0)
    ("'ep" "\\end{proof}" nil 0)
    ("'int" "\\int_{-\\infty}^{\\infty}   \\, dx" nil 0)
    ("'eite" "\\end{itemize}" nil 0)
    ("'bite" "\\begin{itemize}" nil 0)
    ("'mc" "\\multicolumn{2}{c}{}" nil 0)
    ("'count" "k=0,1,\\ldots,N-1" nil 0)
    ("'ef" "\\end{figure}" nil 0)
    ("'ec" "\\end{center}" nil 0)
    ("'case" "\\left\\{\\begin{array}{l}       \\end{array}\\right." nil 0)
    ("'ea" "\\end{array}" nil 0)
    ("predicitve" "predictive" nil 0)
    ("'la" "\\label{eq: }" nil 0)
    ("'bv" "\\begin{verbatim}" nil 0)
    ("'ttt" "test" nil 0)
    ("'bt" "\\begin{tabular}" nil 0)
    ("'bs" "\\begin{slide}{}" nil 0)
    ("'enum" "\\end{enumerate}" nil 0)
    ("'sum" "\\sum_{k=-\\infty}^{\\infty}" nil 0)
    ("'bnum" "\\begin{enumerate}" nil 0)
    ("'bp" "\\begin{proof}" nil 0)
    ("'e" "\\end{}" nil 0)
    ("'b" "\\begin{}" nil 0)
    ("'ecode" "\\end{verbatim}}" nil 0)
    ("'bf" "\\begin{figure}" nil 0)
    ("'pj" "P_{V_{j}}" nil 0)
    ("'bc" "\\begin{center}" nil 0)
    ("'ba" "\\begin{array}" nil 0)
    ("predicitive" "predictive" nil 0)
    ("'eeq" "\\end{equation}" nil 0)
    ("'pd" "\\frac{\\partial }{\\partial}" nil 0)
    ))

(define-abbrev-table 'vc-log-mode-abbrev-table '(
    ))

(define-abbrev-table 'vc-annotate-mode-abbrev-table '(
    ))

(define-abbrev-table 'vc-dired-mode-abbrev-table '(
    ))

(define-abbrev-table 'pike-mode-abbrev-table '(
    ("while" "while" c-electric-continued-statement 0)
    ("else" "else" c-electric-continued-statement 0)
    ))

(define-abbrev-table 'c-mode-abbrev-table '(
    ("while" "while" c-electric-continued-statement 0)
    ("else" "else" c-electric-continued-statement 0)
    ))

(define-abbrev-table 'c++-mode-abbrev-table '(
    ("while" "while" c-electric-continued-statement 0)
    ("else" "else" c-electric-continued-statement 0)
    ("catch" "catch" c-electric-continued-statement 0)
    ))

(define-abbrev-table 'objc-mode-abbrev-table '(
    ("while" "while" c-electric-continued-statement 0)
    ("else" "else" c-electric-continued-statement 0)
    ))

(define-abbrev-table 'java-mode-abbrev-table '(
    ("while" "while" c-electric-continued-statement 0)
    ("finally" "finally" c-electric-continued-statement 0)
    ("else" "else" c-electric-continued-statement 0)
    ("catch" "catch" c-electric-continued-statement 0)
    ))

(define-abbrev-table 'idl-mode-abbrev-table '(
    ))

(define-abbrev-table 'python-mode-abbrev-table '(
    ("reutn" "return" nil 6)
    ("sleep" "import time; time.sleep(1)" nil 1)
    ("exit" "import sys; sys.exit()" nil 5)
    ))

(define-abbrev-table 'comint-mode-abbrev-table '(
    ))

(define-abbrev-table 'shell-mode-abbrev-table '(
    ))

(define-abbrev-table 'plain-tex-mode-abbrev-table '(
    ("'nn" "\\nonumber" nil 0)
    ("'bcode" "{\\small \\begin{verbatim}" nil 0)
    ("'fr" "\\frac{}{}" nil 0)
    ("'eeqa" "\\end{eqnarray*}" nil 0)
    ("'ev" "\\end{verbatim}" nil 0)
    ("'beqa" "\\begin{eqnarray*}" nil 0)
    ("'et" "\\end{tabular}" nil 0)
    ("'beq" "\\begin{equation}" nil 0)
    ("'es" "\\end{slide}" nil 0)
    ("'ep" "\\end{proof}" nil 0)
    ("'int" "\\int_{-\\infty}^{\\infty}   \\, dx" nil 0)
    ("'eite" "\\end{itemize}" nil 0)
    ("'bite" "\\begin{itemize}" nil 0)
    ("'mc" "\\multicolumn{2}{c}{}" nil 0)
    ("'count" "k=0,1,\\ldots,N-1" nil 0)
    ("'ef" "\\end{figure}" nil 0)
    ("'ec" "\\end{center}" nil 0)
    ("'case" "\\left\\{\\begin{array}{l}       \\end{array}\\right." nil 0)
    ("'ea" "\\end{array}" nil 0)
    ("predicitve" "predictive" nil 0)
    ("'la" "\\label{eq: }" nil 0)
    ("'bv" "\\begin{verbatim}" nil 0)
    ("'ttt" "test" nil 0)
    ("'bt" "\\begin{tabular}" nil 0)
    ("'bs" "\\begin{slide}{}" nil 0)
    ("'enum" "\\end{enumerate}" nil 0)
    ("'sum" "\\sum_{k=-\\infty}^{\\infty}" nil 0)
    ("'bnum" "\\begin{enumerate}" nil 0)
    ("'bp" "\\begin{proof}" nil 0)
    ("'e" "\\end{}" nil 0)
    ("'b" "\\begin{}" nil 0)
    ("'ecode" "\\end{verbatim}}" nil 0)
    ("'bf" "\\begin{figure}" nil 0)
    ("'pj" "P_{V_{j}}" nil 0)
    ("'bc" "\\begin{center}" nil 0)
    ("'ba" "\\begin{array}" nil 0)
    ("predicitive" "predictive" nil 0)
    ("'eeq" "\\end{equation}" nil 0)
    ("'pd" "\\frac{\\partial }{\\partial}" nil 0)
    ))

(define-abbrev-table 'latex-mode-abbrev-table '(
    ("'nn" "\\nonumber" nil 0)
    ("'bcode" "{\\small \\begin{verbatim}" nil 0)
    ("'fr" "\\frac{}{}" nil 0)
    ("'eeqa" "\\end{eqnarray*}" nil 0)
    ("'ev" "\\end{verbatim}" nil 0)
    ("'beqa" "\\begin{eqnarray*}" nil 0)
    ("'et" "\\end{tabular}" nil 3)
    ("'beq" "\\begin{equation}" nil 2)
    ("'es" "\\end{slide}" nil 0)
    ("'ep" "\\end{proof}" nil 0)
    ("'int" "\\int_{-\\infty}^{\\infty}   \\, dx" nil 1)
    ("'eite" "\\end{itemize}" nil 0)
    ("'bite" "\\begin{itemize}" nil 0)
    ("'mc" "\\multicolumn{2}{c}{}" nil 0)
    ("'count" "k=0,1,\\ldots,N-1" nil 0)
    ("'ef" "\\end{figure}" nil 3)
    ("'ec" "\\end{center}" nil 4)
    ("'case" "\\left\\{\\begin{array}{l}       \\end{array}\\right." nil 0)
    ("'ea" "\\end{array}" nil 0)
    ("predicitve" "predictive" nil 1)
    ("'la" "\\label{eq: }" nil 0)
    ("'bv" "\\begin{verbatim}" nil 0)
    ("'ttt" "test" nil 0)
    ("'bt" "\\begin{tabular}" nil 3)
    ("'bs" "\\begin{slide}{}" nil 0)
    ("'enum" "\\end{enumerate}" nil 0)
    ("'sum" "\\sum_{k=-\\infty}^{\\infty}" nil 1)
    ("'bnum" "\\begin{enumerate}" nil 0)
    ("'bp" "\\begin{proof}" nil 0)
    ("'e" "\\end{}" nil 0)
    ("'b" "\\begin{}" nil 0)
    ("'ecode" "\\end{verbatim}}" nil 0)
    ("'bf" "\\begin{figure}" nil 3)
    ("'pj" "P_{V_{j}}" nil 0)
    ("'bc" "\\begin{center}" nil 4)
    ("'ba" "\\begin{array}" nil 0)
    ("predicitive" "predictive" nil 0)
    ("'eeq" "\\end{equation}" nil 1)
    ("'pd" "\\frac{\\partial }{\\partial}" nil 0)
    ))

(define-abbrev-table 'slitex-mode-abbrev-table '(
    ))

(define-abbrev-table 'tex-shell-abbrev-table '(
    ))

(define-abbrev-table 'occur-mode-abbrev-table '(
    ))

(define-abbrev-table 'text-mode-abbrev-table '(
    ("'nn" "\\nonumber" nil 1)
    ("'fr" "\\frac{}{}" nil 5)
    ("'bcode" "{\\small \\begin{verbatim}" nil 14)
    ("'eeqa" "\\end{eqnarray*}" nil 15)
    ("'ev" "\\end{verbatim}" nil 2)
    ("'beqa" "\\begin{eqnarray*}" nil 16)
    ("'beq" "\\begin{equation}" nil 32)
    ("'et" "\\end{tabular}" nil 7)
    ("'es" "\\end{slide}" nil 6)
    ("'ep" "\\end{proof}" nil 1)
    ("'eite" "\\end{itemize}" nil 13)
    ("'int" "\\int_{-\\infty}^{\\infty}   \\, dx" nil 5)
    ("'bite" "\\begin{itemize}" nil 17)
    ("'mc" "\\multicolumn{2}{c}{}" nil 1)
    ("'count" "k=0,1,\\ldots,N-1" nil 5)
    ("'ef" "\\end{figure}" nil 1)
    ("'ec" "\\end{center}" nil 2)
    ("'case" "\\left\\{\\begin{array}{l}       \\end{array}\\right." nil 1)
    ("'ea" "\\end{array}" nil 5)
    ("'bv" "\\begin{verbatim}" nil 3)
    ("'la" "\\label{eq: }" nil 4)
    ("predicitve" "predictive" nil 2)
    ("'ttt" "test" nil 2)
    ("'bt" "\\begin{tabular}" nil 6)
    ("'bs" "\\begin{slide}{}" nil 6)
    ("'enum" "\\end{enumerate}" nil 2)
    ("'sum" "\\sum_{k=-\\infty}^{\\infty}" nil 16)
    ("'bp" "\\begin{proof}" nil 1)
    ("'bnum" "\\begin{enumerate}" nil 2)
    ("'e" "\\end{}" nil 4)
    ("'b" "\\begin{}" nil 5)
    ("'ecode" "\\end{verbatim}}" nil 4)
    ("'bf" "\\begin{figure}" nil 2)
    ("'pj" "P_{V_{j}}" nil 4)
    ("'bc" "\\begin{center}" nil 2)
    ("'ba" "\\begin{array}" nil 7)
    ("'eeq" "\\end{equation}" nil 28)
    ("predicitive" "predictive" nil 2)
    ("'pd" "\\frac{\\partial }{\\partial}" nil 1)
    ))

(define-abbrev-table 'lisp-interaction-mode-abbrev-table '(
    ))

(define-abbrev-table 'emacs-lisp-mode-abbrev-table '(
    ))

(define-abbrev-table 'lisp-mode-abbrev-table '(
    ))

(define-abbrev-table 'fundamental-mode-abbrev-table '(
    ))

(define-abbrev-table 'global-abbrev-table '(
    ("perioidized" "periodized" nil 9)
    ("algortime" "algoritme" nil 4)
    ("eqaution" "equation" nil 1)
    ("loaction" "location" nil 1)
    ))
