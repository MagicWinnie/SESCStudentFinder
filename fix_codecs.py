import codecs

with codecs.open("output.json", "rb", "unicode_escape") as my_input:
    contents = my_input.read()

with codecs.open("output.json", "wb", "utf8") as my_output:
    my_output.write(contents)