import readable_text
import sys

readable_text.render("""
test title
==========

a
b
  c
  c

tX title
---------
> q1
> q2

### ttx title
 * a
 * b
  * c
  * d
 * e
  1. f
     continue
  2. h
  3. i
  4. j
  5. k
  6. l
  7. m
  8. n
    * a
       continue
     > quotex
     > quotey
    * b
    continue
  9. o
 10. p
 11. q

 * d
* d * **c** \\*d

  1. a
 * b
  2. a
  * b
  3. a
   * b
  4. a
    * b
  5. a
  b
  6. a
   b
  7. a
    b

""", sys.stdout)

