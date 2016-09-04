import simple_format
import sys

sys.stdout.write("""
<html>
 <head>
  <title>test</title>
  <meta charset="utf-8">
 </head>
 <body>
""")

simple_format.render_as_html("""
Luctus et ultrices posuere cubilia Curae; Curabitur consequat leo.
==================================================================

Congue nihil imperdiet *doming id quod mazim placerat* facer possim assum. Typi
non habent claritatem insitam; est usus legentis in iis qui facit eorum
claritatem. Investigationes demonstraverunt lectores legere me lius quod ii
legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem
consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus
parum claram, anteposuerit **litterarum formas humanitatis** per seacula quarta
decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari,
fiant sollemnes in futurum.

Nunc varius risus quis nulla. Vivamus vel magna. Ut rutrum. Aenean dignissim,
leo quis faucibus semper, *massa est **faucibus** massa,* sit amet pharetra arcu nunc
et sem. Aliquam tempor. **Nam lobortis sem *non* urna.** <Pellentesque> et \*urna sit
amet leo accumsan volutpat. Nam molestie lobortis lorem. Quisque eu nulla.
Donec id orci in ligula dapibus egestas. Donec sed velit ac lectus mattis
sagittis.

Rutrum, nisl elit pharetra purus, non interdum nibh enim.
---------------------------------------------------------

In hac habitasse platea dictumst. Maecenas in ligula. Duis tincidunt odio
sollicitudin quam. Nullam non mauris. Phasellus lacinia, velit sit amet
bibendum euismod, leo diam interdum ligula, eu scelerisque sem purus in tellus.

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. In sit amet nunc id
quam porta varius. Ut aliquet facilisis turpis. Etiam pellentesque quam et
erat. Praesent suscipit justo.

Laoreet, est sed gravida tempor, nibh.
  1. Sem, eu congue metus ligula sed.
  2. Bibendum odio sit amet neque. Integer.
    * Erat. Phasellus luctus cursus risus. Phasellus.
    * Duis lobortis, metus eu laoreet tristique.
      > Leo sollicitudin consequat. Aliquam lobortis. 
      > In eu justo. Nunc vitae.
      >  * list item 1 in quote
      >  * list item 2 in quote
      > Egestas. Sed vitae eros. Nulla.
    * Tempor vel, aliquet ut, eros. In.
  3. Enim mauris, suscipit a, auctor et.
    1. Amet, sem.
    2. Ac dui. In ac urna non.
      * Amet, consectetuer adipiscing elit. Sed volutpat.
      * Venenatis. Vivamus dui. Nunc accumsan, quam.
    3. Orci luctus et ultrices posuere cubilia.
    4. Class aptent taciti sociosqu ad.
  4. Sit amet malesuada tortor nisi sit.  Decima. Eodem modo typi, qui nunc
     nobis videntur parum clari, fiant sollemnes in futurum.  Nunc varius risus
     quis nulla. Vivamus vel magna. Ut rutrum. Aenean dignissim, leo quis faucibus
     semper, massa est.
  5. Id quam porta varius. Ut aliquet.
  6. Claritatem. Investigationes demonstraverunt lectores legere me.
  7. Ipsum dolor sit amet, consectetuer adipiscing.
  8. Et, massa. Nulla sed erat vel.
  9. Posuere cubilia Curae; Maecenas interdum purus.
 10. Sodales nec, purus. Morbi aliquet risus.
 11. Amet mauris. Curabitur a quam. Aliquam.
 12. Eget, iaculis quis, tristique adipiscing, diam. 
 13. Sem, eu tempor nisi felis et.
 14. Porttitor ipsum at ipsum. Nam massa. 
 15. Gravida. Class aptent taciti sociosqu ad.


Cras nec metus pulvinar sem tempor hendrerit. Class aptent taciti sociosqu ad
litora torquent per conubia nostra, per inceptos himenaeos. Nullam in nulla.
Mauris elementum. Curabitur tempor, quam ac rutrum placerat, nunc augue
ullamcorper est, vitae molestie neque nunc a nunc. Integer justo dolor,
consequat id, rutrum auctor, ullamcorper sed, orci. In hac habitasse platea
dictumst. Fusce euismod semper orci. Integer venenatis quam non nunc. Vivamus
in lorem a nisi aliquet commodo. Suspendisse massa lorem, dignissim at,
vehicula et, ornare non, libero. Donec molestie, velit quis dictum scelerisque,
est lectus hendrerit lorem, eget dignissim orci nisl sit amet massa. Etiam
volutpat lobortis eros. Nunc ac tellus in sapien molestie rhoncus. Pellentesque
nisl. Praesent venenatis blandit velit. Fusce rutrum. Cum sociis natoque
penatibus et magnis dis parturient montes, nascetur ridiculus mus. Pellentesque
vitae erat. Vivamus porttitor cursus lacus. Pellentesque tellus. Nunc aliquam
interdum felis. Nulla imperdiet leo. Mauris hendrerit, sem at mollis pharetra,
leo sapien pretium elit, a faucibus sapien dolor vel pede. Vestibulum et enim
ut nulla sollicitudin adipiscing. Suspendisse malesuada venenatis mauris.
Curabitur ornare mollis velit. Sed vitae metus. Morbi posuere mi id odio. Donec
elit sem, tempor at, pharetra eu, sodales sit amet, elit.

### Et ultrices posuere cubilia Curae; Vestibulum.

  1. Curabitur urna tellus, aliquam vitae, ultrices eget, vehicula nec, diam.
     Integer elementum, felis non faucibus euismod, erat massa dictum eros, eu
     ornare ligula tortor et mauris. Cras molestie magna in nibh. Aenean et
     tellus.  Fusce adipiscing commodo erat. In eu justo. Nulla dictum, erat
     sed blandit venenatis, arcu dolor molestie dolor, vitae congue orci risus
     a nulla.  Pellentesque sit amet arcu. In mattis laoreet enim. Pellentesque
     id augue et arcu blandit tincidunt. Pellentesque elit ante, rhoncus quis,
     dapibus sit amet, tincidunt eu, nibh. In imperdiet. Nunc lectus neque,
     commodo eget, porttitor quis, fringilla quis, purus.

  2. Vulputate ac, pede. Donec vestibulum purus non tortor. Integer at nunc.

  3. Suspendisse fermentum velit quis sem. Phasellus suscipit nunc in risus.
     Nulla sed lectus. Morbi sollicitudin, diam ac bibendum scelerisque, enim
     tortor.

  4. Vitae, nunc. Pellentesque habitant morbi tristique senectus et netus et
     malesuada fames ac turpis egestas. Praesent lacus diam, auctor quis, venenatis
     in, hendrerit at, est. Vivamus eget eros.

     Phasellus congue, sapien ac iaculis
     feugiat, lacus lacus accumsan lorem, quis volutpat justo turpis ac mauris.

     Duis velit magna, scelerisque vitae, varius ut, aliquam.

Fusce ac elit ut elit aliquam suscipit. Duis leo est, interdum nec, varius in,
facilisis vitae, odio. Phasellus eget leo at.

> Nunc non mauris. Nam accumsan tortor gravida elit. Cras porttitor.
> 
> Praesent vel enim sed eros luctus imperdiet. Mauris neque ante, placerat at,
> mollis vitae, faucibus quis, leo. Ut feugiat. Vivamus urna quam.


Duis sagittis dignissim eros. In sit amet lectus. Fusce lacinia mauris vitae
nisl interdum condimentum. Etiam in magna ac nibh ultrices vehicula. Maecenas
commodo facilisis lectus. Praesent sed mi. Phasellus ipsum. Donec quis tellus
id lectus faucibus molestie. Praesent vel ligula. Nam venenatis neque quis
mauris. Proin felis. Cum sociis natoque penatibus et magnis dis parturient
montes, nascetur ridiculus mus. Aliquam quam. Nam felis velit, semper nec,
aliquam nec, iaculis vel, mi. Nullam et augue vitae nunc tristique vehicula.
Suspendisse eget elit. Duis adipiscing dui non quam.

-------

Porttitor.

Praesent vel enim sed eros luctus imperdiet. Mauris neque ante, placerat at,
mollis vitae, faucibus quis, leo. Ut feugiat. Vivamus urna quam, congue
vulputate, convallis non, cursus cursus, risus. Quisque aliquet. 

中
文
测
试

""", sys.stdout)

sys.stdout.write("""
 </body>
<html>
""")
