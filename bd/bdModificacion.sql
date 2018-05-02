alter table cloud AUTO_INCREMENT=1;

alter table nodos AUTO_INCREMENT=1;

alter table methodData AUTO_INCREMENT=1;

alter table methodData modify contenido mediumtext;

alter table methodData modify contenido mediumtext character set utf8 collate utf8_general_ci; 

alter table methodData modify contenido mediumtext character set latin1 collate latin1_bin;

