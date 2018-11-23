import os
import json 
import numpy as np


from scipy import spatial




os.environ['BERT_BASE_DIR'] = 'multilingual_L-12_H-768_A-12'

"""lyric1 = "Spent 24 hours \n\
I need more hours with you \n\
You spent the weekend \n\
Getting even ooh ooh \n\
We spent the late nights \n\
Making things right, between us \n\
But now it's all good baby \n\
Roll that Backwood baby \n\
And play me close \n\
'Cause girls like you \n\
Run around with guys like me \n\
Til sundown, when I come through \n\
I need a girl like you, yeah yeah \n\
Girls like you \n\
Love fun, yeah me too \n\
What I want when I come through \n\
I need a girl like you, yeah yeah \n\
Yeah yeah yeah \n\
Yeah yeah yeah \n\
I need a girl like you, yeah yeah\n\
Yeah yeah yeah\n\
Yeah yeah yeah\n\
I need a girl like you, yeah yeah\n\
I spent last night\n\
On the last flight to you\n\
Took a whole day up\n\
Trying to get way up, ooh ooh\n\
We spent the daylight\n\
Trying to make things right between us\n\
And now it's all good baby\n\
Roll that Backwood baby\n\
And play me close\n\
'Cause girls like you\n\
Run around with guys like me\n\
'Til sundown, when I come through\n\
I need a girl like you, yeah yeah\n\
Girls like you\n\
Love fun, yeah me too\n\
What I want when I come through\n\
I need a girl like you, yeah yeah\n\
Yeah yeah yeah\n\
Yeah yeah yeah\n\
I need a girl like you, yeah yeah\n\
Yeah yeah yeah\n\
Yeah yeah yeah\n\
I need a girl like you, yeah yeah\n\
I need a girl like you, yeah yeah\n\
I need a girl like you\n\
Maybe it's 6:45\n\
Maybe I'm barely alive\n\
Maybe you've taken my shit for the last time, yeah\n\
Maybe I know that I'm drunk\n\
Maybe I know you're the one\n\
Maybe I'm thinking it's better if you drive\n\
'Cause girls like you\n\
Run around with guys like me\n\
'Til sundown, when I come through\n\
I need a girl like you, yeah yeah\n\
'Cause girls like you\n\
Run around with guys like me\n\
'Til sundown, when I come through\n\
I need a girl like you, yeah yeah\n\
Girls like you\n\
Love fun, yeah me too\n\
What I want when I come through\n\
I need a girl like you, yeah yeah\n\
Yeah yeah yeah\n\
Yeah yeah yeah\n\
I need a girl like you, yeah yeah\n\
Yeah yeah yeah\n\
Yeah yeah yeah\n\
I need a girl like you"


lyric2 = "Spent 24 hours\n\
I need more hours with you\n\
You spent the weekend\n\
Becoming equal, ooh ooh\n\
We spent the late nights\n\
Do things right, between us\n\
But now everything is fine, baby\n\
Roll the backwood baby\n\
And play me around\n\
Because girls like you\n\
Running around with guys like me\n\
Until sunset, when I come through\n\
I need a girl like you, yes, yes\n\
Girl like you\n\
Love fun, yeah me too\n\
What I want, when I get through\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you, yes, yes\n\
I spent last night\n\
On the last flight to you\n\
I needed a whole day\n\
Try to get up, ooh ooh\n\
We spent the daylight\n\
Try to get things right between us\n\
And now everything is fine, baby\n\
Roll the backwood baby\n\
And play me around\n\
Because girls like you\n\
Running around with guys like me\n\
Until sunset, when I come through\n\
I need a girl like you, yes, yes\n\
Girl like you\n\
Love fun, yeah me too\n\
What I want, when I get through\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you, yes, yes\n\
I need a girl like you, yes, yes\n\
I need a girl like you\n\
Maybe it's 6:45\n\
Maybe I'm barely alive\n\
Maybe you took my shit for the last time, yes\n\
Maybe I know that I'm drunk\n\
Maybe I know that you are the one\n\
Maybe I think it's better if you drive\n\
Because girls like you\n\
Running around with guys like me\n\
Until sunset, when I come through\n\
I need a girl like you, yes, yes\n\
Because girls like you\n\
Running around with guys like me\n\
Until sunset, when I come through\n\
I need a girl like you, yes, yes\n\
Girl like you\n\
Love fun, yeah me too\n\
What I want, when I get through\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you, yes, yes\n\
Yes Yes Yes\n\
Yes Yes Yes\n\
I need a girl like you"
"""




lyric1 = "Trap, TrapMoneyBenny\n\
This shit got me in my feelings\n\
Gotta be real with it, yup\n\
Kiki, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I need ya\n\
And I'm down for you always\n\
KB, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I need ya\nAnd I'm down for you always\n\
Look, the new me is really still the real me\n\
I swear you gotta feel me before they try and kill me\n\
They gotta make some choices, they runnin' out of options\n\
'Cause I've been going off and they don't know when it's stopping\n\
And when you get to topping\nI see that you've be\en learning\n\
And when I take you shopping\n\
you spend it like you earned it\n\
And when you popped off on your ex, he deserved it\n\
I thought you were the one from the jump that confirmed it\n\
TrapMoneyBenny\nI buy you Champagne but you love some Henny\n\
From the block, like you Jenny\n\
I know you special, girl, 'cause I know too many\n\
'Resha, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I need ya\n\
And I'm down for you always\n\
J.T., do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I need ya\n\
And I'm down for you always\n\
Two bad bitches and we kissin' in the Wraith\n\
Kissin'-kissin' in the Wraith, kiss-kissin' in the Wraith\n\
I need that black card and the code to the safe\n\
Code to the safe, code-code to the safe-safe\n\
I show him how that neck work\n\
Fuck that Netflix and chill\n\
What's your net-net-net worth?\n\
'Cause I want ya, and I need ya\n\
And I'm down for you always\n\
(Yea, yea, yea, yea, he bad)\n\
And I'm down for you always\n\
(Yea, yea, yea, guess who's back)\n\
And I'm down for you always\n\
D-down for you al-\n\
(Black biggy biggy black biggy black blake)\n\
D-d-down for you always\n\
(I got a new boy, and that nigga trade!)\n\
Kiki, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want you, and I need ya\n\
And I'm down for you always\n\
KB, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I\n\
Skate and smoke and ride\n\
Now let me see you\n\
Bring that ass, bring that ass, bring that ass back\n\
Bring that ass, bring that ass, bring that ass back\n\
Now let me see you\n\
Shawty say the nigga that she with can’t hit\n\
But shawty, I’ma hit it, hit it like I can’t miss\n\
Now let me see you\n\
Walk that ass, you’re the only one I love\n\
(Walk that ass, walk-walk that ass)\n\
Now let me see you\n\
(Bring that ass back)\n\
Now let me see you\n\
(W-w-walk that ass, you’re the only one I love)\n\
Now let me see you, now let me see you\n\
(Let’s go, let’s go, let’s go)\n\
Now let me see you\n\
(Bring that ass back)\n\
Trap, TrapMoneyBenny\n\
This shit got me in my feelings\n\
I just gotta be real with it, yup\n\
BlaqNmilD, you a genius, you diggin' me?\n\
What are you all talking about?\n\
You don't know that? I don't even care \n\
I need a photo with Drake\n\
Because my instagram's weak as fuck\n\
I'm just being real, my shit look."


lyric2 = "Trap, TrapMoneyBenny\n\
This shit got me in my feelings\n\
Gotta be real with it, yup\n\
Kiki, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
Cause I want ya, and I need ya\n\
And I'm down for you always\n\
KB, do you love me? Are you riding?\n\
Say you'll never ever leave from beside me\n\
'Cause I want ya, and I need ya\n\
And I'm down for you always\n\
Look, the new me is really still the real me\n\
I swear you gotta feel me before they try and kill me\n\
They gotta make some choices, they runnin' out of options\n\
'Cause I've been going off and they don't know when it's stopping\n\
And when you get to topping\n\
I see that you've been learning\n\
And when I take you shopping\n\
 you spend it like you earned it\n\
 And when you popped off on your ex, he deserved it\n\
 I thought you were the one from the jump that confirmed it\n\
 TrapMoneyBenny\n\
 I buy you Champagne but you love some Henny\n\
 From the block, like you Jenny\n\
 I know you special, girl, 'cause I know too many\n\
 'Resha, do you love me? Are you riding?\n\
 Say you'll never ever leave from beside me\n\
 'Cause I want ya, and I need ya\n\
 And I'm down for you always\n\
 J.T., do you love me? Are you riding?\n\
 Say you'll never ever leave from beside me\n\
 'Cause I want ya, and I need ya\n\
 And I'm down for you always\n\
 Two bad bitches and we kissin' in the Wraith\n\
 Kissin'-kissin' in the Wraith, kiss-kissin' in the Wraith\n\
 I need that black card and the code to the safe\n\
 Code to the safe, code-code to the safe-safe\n\
 I show him how that neck work\n\
 Fuck that Netflix and chill\n\
 What's your net-net-net worth?\n\
 'Cause I want ya, and I need ya\n\
 And I'm down for you always\n\
 (Yea, yea, yea, yea, he bad)\n\
 And I'm down for you always\n\
 (Yea, yea, yea, guess who's back)\n\
 And I'm down for you always\n\
 D-down for you al-\n\
 (Black biggy biggy black biggy black blake)\n\
 D-d-down for you always\n\
 (I got a new boy, and that nigga trade!)\n\
 Kiki, do you love me? Are you riding?\n\
 Say you'll never ever leave from beside me\n\
 'Cause I want you, and I need ya\n\
 And I'm down for you always\n\n\
 KB, do you love me? Are you riding?\n\
 Say you'll never ever leave from beside me\n\
 'Cause I want ya, and I\n\n\
 Skate and smoke and ride\n\
 Now let me see you\n\
 Bring that ass, bring that ass, bring that ass back\n\
 Bring that ass, bring that ass, bring that ass back\n\
 Now let me see you\n\
 Shawty say the nigga that she with can’t hit\n\
 But shawty, I’ma hit it, hit it like I can’t miss\n\
 Now let me see you\n\
 Walk that ass, you’re the only one I love\n\
 (Walk that ass, walk-walk that ass)\n\
 Now let me see you\n(Bring that ass back)\n\
 Now let me see you\n\
 (W-w-walk that ass, you’re the only one I love)\n\
 Now let me see you, now let me see you\n\
 (Let’s go, let’s go, let’s go)\n\
 Now let me see you\n(Bring that ass back)\n\
 Trap, TrapMoneyBenny\n\
 This shit got me in my feelings\n\
 I just gotta be real with it, yup\n\
 BlaqNmilD, you a genius, you diggin' me?\n\
 What are you all talking about?\n\
 You don't know that? I don't even care\n\
 I need a photo with Drake"

rows_lyric_1= lyric1.split("\n")
rows_lyric_2 = lyric2.split("\n")


print("Length 1:" + str(len(rows_lyric_1)))
print("Length 2:" + str(len(rows_lyric_2)))

assert len(rows_lyric_1) == len(rows_lyric_2)
print("Same length...OK")

with open('lyric1.txt', 'w',encoding="utf-8") as outfile1:
    for r in rows_lyric_1:  
        #print(str(r) + "\n")
        outfile1.write(str(r) + "\n")

with open('lyric2.txt', 'w',encoding="utf-8") as outfile2:
       for r in rows_lyric_2:  
        #print(str(r) + "\n")
        outfile2.write(str(r) + "\n")
    
print("Extracting features lyrics 1.........")

os.system(
            'python3 extract_features.py \
              --input_file=lyric1.txt \
              --output_file=output1.txt \
              --vocab_file=$BERT_BASE_DIR/vocab.txt \
              --bert_config_file=$BERT_BASE_DIR/bert_config.json \
              --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
              --layers=-2 \
              --max_seq_length=128 \
              --batch_size=8'
        )

print("Extracting features lyrics 2.........")

os.system(
            'python3 extract_features.py \
              --input_file=lyric2.txt \
              --output_file=output2.txt \
              --vocab_file=$BERT_BASE_DIR/vocab.txt \
              --bert_config_file=$BERT_BASE_DIR/bert_config.json \
              --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
              --layers=-2 \
              --max_seq_length=128 \
              --batch_size=8'
        )


fin = open("output1.txt",'r', encoding="utf-8")
lines1 = fin.readlines()
fin.close()

means_vec1 = []

for index, l in enumerate(lines1):
    
        data = json.loads(l)
        features = data['features']
        tokens_features = []

        for f in features:
            if str(f['token'])=='[CLS]' or str(f['token'])=='[SEP]':
                continue
            tokens_features.append(list(f['layers'][0]['values']))

        mean = np.mean(tokens_features, axis=0)
        means_vec1.append(mean)

        

fin = open("output2.txt",'r', encoding="utf-8")
lines2 = fin.readlines()
fin.close()

means_vec2 = []

for index, l in enumerate(lines2):
    
        data = json.loads(l)
        features = data['features']
        tokens_features = []

        for f in features:
            if str(f['token'])=='[CLS]' or str(f['token'])=='[SEP]':
                continue
            tokens_features.append(list(f['layers'][0]['values']))

        mean = np.mean(tokens_features, axis=0)
        means_vec2.append(mean)

print(len(means_vec1))
print(len(means_vec2))

assert len(means_vec1) == len(means_vec2)


for i in range(len(means_vec1)):
    dist = 1 - spatial.distance.cosine(means_vec1[i],means_vec2[i])
    #dist = np.linalg.norm(means_vec1[i]-means_vec2[i])
    print("Sentence 1:" + str(rows_lyric_1[i]))
    print("Sentence 2:" + str(rows_lyric_2[i]))
    print("Cosine Similarity: " + str(dist))
    print("\n\n\n")
#assert means_vec1 == means_vec2




