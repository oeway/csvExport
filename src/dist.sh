rm -rf ../*.app 
python setup.py py2app -A
cp -r dist/* ../
rm -rf build dist
