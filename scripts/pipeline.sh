#! bash
set -x

bash scripts/download_data.sh && \
bash scripts/decompress_select.sh && \
bash scripts/join.sh