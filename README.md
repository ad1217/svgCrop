# svgCrop #

I wouldn't exactly describe this as done, but it's a thing to automatically crop the output of [Write](http://www.styluslabs.com/). Primarilly written for use in Emacs' Org mode. Requires Inkscape for getting size info.

## Standalone ##

Call with 

    svgCrop.py <input.svg> <output.svg> [margin]
    
where `margin` is in pixels. If it is omitted, it is assumed to be 0.

## Org mode usage ##

Not really finished, still a bit clunky.

Jam this in your `.org` file:
```org
#+NAME: svgCrop
#+BEGIN_SRC emacs-lisp :var inFile="" :var margin="50" :exports none
  (let ((outFile (replace-regexp-in-string ".svg$" "-cropped.svg" inFile)))
   (call-process "/home/adam/Programs/mystuff/svgCrop/svgCrop.py" nil nil nil inFile outFile margin)
   outFile)
#+END_SRC
```

And this in your emacs init file:
```elisp
(defun org-run-write-stylus ()
  (interactive)
  (let ((target-dir (concat default-directory "drawings/")))
    (unless (file-exists-p target-dir) (make-directory target-dir))
    (let ((inFile
           (substring (shell-command-to-string
                       (concat "mktemp --suffix .html -p " target-dir))
                      0 -1)))
    (start-process "write-stylus" "write stylus output" "write_stylus" inFile)
    (insert
     (concat "# eval to edit: (start-process \"write-stylus\""
             "\"write stylus output\" \"write_stylus\" \"" inFile "\")\n"
             "#+CALL: svgCrop(\""
             (replace-regexp-in-string ".html$" "_page001.svg" inFile)
             "\") :results file")))))
```

then call `org-run-write-stylus`, and it will open Write with a new file and insert a `#+CALL` at point that will crop your SVG. To do this manually, insert: `#+CALL: svgCrop(<input.svg>[, margin]) :results file` (as shown, you can also set the margin here).


Hopefully I'll make this less clunky later, and maybe port the python bit to elisp. Ideally, I'd also like to get rid of the Inkscape dependency, as that seems silly.
