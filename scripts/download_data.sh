#! bash

set -x

# Make directories
mkdir -p data/compressed

# Download metadata
curl -L https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland/raw/master/SARS-CoV-2-Sequenzdaten_Deutschland.csv.xz \
> data/compressed/metadata.csv.xz

# Download lineage data
curl -L https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland/raw/master/SARS-CoV-2-Entwicklungslinien_Deutschland.csv.xz \
> data/compressed/lineages.csv.xz


