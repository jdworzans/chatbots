import editdistance

def scaled_editdist(ans, cor):
    ans = ans.lower()
    cor = cor.lower()  
    return editdistance.eval(ans, cor) / len(cor)
    
def single_match(a, c):
    if c.isdecimal():
        return a == c
    return scaled_editdist(a, c) < 0.5
        
def match(ans, cor):
    # return any(single_match(ans, c) for c in cor)
    return single_match(ans, cor)

found_answers = list()
for x in open('found_answers.txt'):
    x = x.strip()
    found_answers.append(x.lower())

correct_answers = list()
for x in open('correct_answers.txt'):
    x = x.strip()
    correct_answers.append(x.lower().split('\t'))
    
N = len(correct_answers)
score = 0.0

for ans, cor in zip(found_answers, correct_answers[0:len(found_answers)]):    
    if match(ans, cor[0]):
        score += 1
        
print('TOTAL SCORE:', score)    
