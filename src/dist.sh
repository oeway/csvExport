rm -rf ../*.app 
python setup.py py2app -A
cp -R dist/* ../
rm -rf build dist
