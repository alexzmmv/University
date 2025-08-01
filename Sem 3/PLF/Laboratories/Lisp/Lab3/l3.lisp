(defun replace-node (old-node new-node tree)
  (if (null tree)
      nil
      (if (equal old-node (car tree))
          (cons new-node (replace-node-in-subtrees old-node new-node (cdr tree)))
          (cons (car tree) (replace-node-in-subtrees old-node new-node (cdr tree))))))

(defun replace-node-in-subtrees (old-node new-node subtrees)
  (if (null subtrees)
      nil
      (cons (replace-node old-node new-node (car subtrees))
            (replace-node-in-subtrees old-node new-node (cdr subtrees)))))


; (replace-node 'a 'g '(a (b) (a (c) (d)) (e) (a (f) (g))))
; (replace-node 'a 'g '(a))
; (replace-node 'a 'g '(b))
;replace node a with g in a tree with 10 nodes all a
; (replace-node 'a 'g '(a (a) (a) (a) (a) (a) (a) (a (a) (a)) (a) (a) (a) (a)))