#! /bin/bash

for letter in A B C D E F G H I L M N O P Q R S T U V W X Y Z; do
  cat >| "$letter.md" <<EOS
---
layout: letter
letter: $letter
---
EOS
done