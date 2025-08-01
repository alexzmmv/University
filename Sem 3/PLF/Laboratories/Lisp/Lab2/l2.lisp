(defun find-level (node tree current-level)
  (if (null tree)
      nil
      (if (equal node (car tree))
          current-level 
          (find-level-in-subtrees node (cdr tree) (+ current-level 1))))) 

(defun find-level-in-subtrees (node subtrees current-level)
  (if (null subtrees)
      nil 
      (let ((result (find-level node (car subtrees) current-level)))
        (if result
            result 
            (find-level-in-subtrees node (cdr subtrees) current-level))))) 

(defun node-level (node tree)
  (find-level node tree 0))

(node-level 'D '(A (B) (C (D) (E)))) 
;(node-level '2 '(A (B) (C (D) (E)))) 
;(node-level 'E '(A (B) (C (D) (E)))) 
;(node-level 'Z '(A (B) (C (D) (E)))) 

;6 L3
