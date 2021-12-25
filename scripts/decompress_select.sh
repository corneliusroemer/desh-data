#! bash
set -x

xzcat data/compressed/metadata.csv.xz \
| xsv select IMS_ID,DATE_DRAW,SEQ_REASON,PROCESSING_DATE,SENDING_LAB_PC,SEQUENCING_LAB_PC \
> data/metadata.csv

xzcat data/compressed/lineages.csv.xz \
| xsv select IMS_ID,lineage,scorpio_call \
> data/lineages.csv