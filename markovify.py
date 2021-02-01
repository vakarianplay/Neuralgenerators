import markovify

#file.txt - your dataset file
with open("file.txt",encoding='utf-8') as f:
    text = f.read()
    
text_model = markovify.Text(text)
for i in range(5):
    print(text_model.make_sentence())
for i in range(10):
    print(text_model.make_short_sentence(380))
