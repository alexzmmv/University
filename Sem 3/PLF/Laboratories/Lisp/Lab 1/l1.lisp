;a
(defun dot-product (l1 l2)
    (if (or (null l1) (null l2))
      0
      (+ (* (car l1) (car l2)) (dot-product (cdr l1) (cdr l2)))))

;(dot-product '(1 2 3 5) '(4 5 6 7))

;b
(defun mymax (a b)
  (cond
    ((null a) b)
    ((null b) a)
    ((> a b) a)
    (t b)))

(defun max-heterogeneous (l1)
  (cond
    ((null l1) nil)
    ;if list
    ((listp (car l1))
     (mymax (max-heterogeneous (car l1))
          (max-heterogeneous (cdr l1))))
    ;if number
    ((numberp (car l1))
     (let ((cdr-max (max-heterogeneous (cdr l1))))
       (if cdr-max
           (mymax (car l1) cdr-max)
           (car l1))))
    ;else
    (t (max-heterogeneous (cdr l1)))))

;(max-heterogeneous '(a b (1 2 3 (a b c 10 z 3) 8) 4))

(defun basic-expression (op a b)
	(cond
		((string= op "+") (+ a b))
		((string= op "-") (- a b))
		((string= op "*") (* a b))
		((string= op "/") (floor a b))
	)
)

(defun expression (l)
    (cond
        ((null l) nil)
        ((and (and (numberp (cadr l)) (numberp (caddr l))) (atom (car l))) (cons (basic-expression (car l) (cadr l) (caddr l)) (expression (cdddr l))))
        (T (cons (car l) (expression (cdr l))))
    )
)

(defun solve (l)
    (cond
        ((null (cdr l)) (car l))
        (T (solve (expression l)))
    )
)
;(solve '(+ * 2 4 3))
;d
(defun even_length (l)
    (cond
        ((null l) T)
        ((null (cdr l)) nil)
        (T (even_length (cddr l)))
    )
)

;(even_length '(1 2 3 4 5 6 7 8 9 10))
;(even_length '(1 2 3 4 5 6 7))

;L2 10