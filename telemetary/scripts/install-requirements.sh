if [ $1 ]; then requirement=$1
else requirement="/requirements.txt"
fi

for word in $(grep dronekit ${requirement} -w -v); do
  package="${package} '${word}'";
done

command="pip3 install --target=/install $package";
eval $command