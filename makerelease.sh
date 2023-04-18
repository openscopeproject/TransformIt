#!/bin/bash

TAG=$(git describe --tags)
TAG=${TAG#v}
METADATATAG=$(git describe --tags --abbrev=0)
METADATATAG=${METADATATAG#v}
mkdir -p releases/$TAG
ARCHIVE="releases/$TAG/TransformIt.zip"
if [ -f "$ARCHIVE" ]; then
    rm "$ARCHIVE"
fi
zip -r "$ARCHIVE" TransformIt -x \*_test.py \*.pyc \*.log \*.ini \*.gitattributes '*__pycache__*'
echo "Created $ARCHIVE"

mkdir -p releases/tmp/resources
cp icon/icon_64.png releases/tmp/resources/icon.png
cp metadata_template.json releases/tmp/metadata.json
sed -i "s/%RELEASE_VERSION_TAG/$METADATATAG/g" releases/tmp/metadata.json
unzip "$ARCHIVE" -d releases/tmp/
mv releases/tmp/TransformIt releases/tmp/plugins

cd releases/tmp
PCM_ARCHIVE="../$TAG/TransformIt_v"$TAG"_pcm.zip"
if [ -f "$PCM_ARCHIVE" ]; then
    rm "$PCM_ARCHIVE"
fi
zip -r "$PCM_ARCHIVE" *
cd ..
rm -rf ./tmp
echo "Created PCM archive"
