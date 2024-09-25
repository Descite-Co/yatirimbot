# confirmation_script.sh
#!/bin/sh
echo "Do you want to proceed with the commit? (y/n)"
read answer
if [ "$answer" != "y" ]; then
    echo "Aborting commit."
    exit 1
fi
