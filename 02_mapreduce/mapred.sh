#!/bin/bash

mapper=${ROOT_DIR}/mapper/test.map.py
reducer=${ROOT_DIR}/reducer/test.reduce.py

access_gz=/access/${YESTERDAY}/*.ncsa.gz
attack_gz=/attack/${YESTERDAY}/*.ncsa.gz

STREAM=/usr/share/dse/hadoop/lib/hadoop-streaming-1.0.4.2.jar

mapper=${ROOT_DIR}/mapper/ncsa.map.py
lib_secrule=${ROOT_DIR}/mapper/secrule.py
combiner=${ROOT_DIR}/reducer/ncsa.jldrp.awk
reducer=${ROOT_DIR}/reducer/ncsa.jldrp.awk

hadoop jar $STREAM -input ${access_gz} -input ${attack_gz} \
	-output ${out} \
	-file ${mapper} \
	-file ${lib_secrule} \
	-file ${reducer}  \
	-mapper ${mapper} \
	-combiner ${combiner} \
	-reducer ${reducer} \
	-jobconf stream.recordreader.compression=gzip
