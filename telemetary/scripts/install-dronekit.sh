# if [ $1 ]; then requirement=$1
# else requirement="/requirements.txt"
# fi

# dronekit=$(grep dronekit ${requirement});
# if [ $dronekit ]; then
  dronekit="dronekit"

  sed -i 's/, int,/, unsigned int,/' /usr/include/assert.h
  pip3 install --install-option="--prefix=/install" "${dronekit}";
  sed -i 's/, unsigned int,/, int,/' /usr/include/assert.h
# fi