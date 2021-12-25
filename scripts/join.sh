#! bash

set -x

xsv join IMS_ID data/metadata.csv IMS_ID data/lineages.csv \
| xsv select '!IMS_ID[1]' - \
> data/meta_lineages.csv