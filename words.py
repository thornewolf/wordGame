import random
words = []
with open('words.txt') as f:
    words = f.read().split()
swords = set(words)

memo = {}
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    cost = 0 if s[-1] == t[-1] else 1
       
    i1 = (s[:-1], t)
    if not i1 in memo:
        memo[i1] = levenshtein(*i1)
    i2 = (s, t[:-1])
    if not i2 in memo:
        memo[i2] = levenshtein(*i2)
    i3 = (s[:-1], t[:-1])
    if not i3 in memo:
        memo[i3] = levenshtein(*i3)
    res = min([memo[i1]+1, memo[i2]+1, memo[i3]+cost])
    
    return res

def get_naive_perms(word):
    alts = []
    # All letter remove options
    for i in range(len(word)):
        if len(word) == 1:
            break
        alts.append(word[:i]+word[i+1:])
    # All letter add options
    for i in range(len(word)+1):
        for c in [chr(i) for i in range(ord('a'), ord('z')+1)]:
            alts.append(word[:i] + c + word[i:])
    # All letter replace options
    for i in range(len(word)):
        for c in [chr(i) for i in range(ord('a'), ord('z')+1)]:
            if c == word[i]:
                continue
            alts.append(word[:i]+ c + word[i+1:])
    return alts

def get_valid_subset(word_list):
    return [word for word in word_list if word in swords]

def get_valid_plays(word):
    return get_valid_subset(get_naive_perms(word))

def gen_dictionary_valid_plays():
    plays = []
    word_sample = random.sample(words, 10)
    for i,word in enumerate(word_sample):
        plays.append(get_valid_subset(get_naive_perms(word)))
    print(*zip(word_sample,plays[:3]), sep='\n')

def test_get_naive_perms():
    TEST_WORD = 'a'
    print(TEST_WORD)
    print(get_naive_perms(TEST_WORD))

def test_get_valid_subset():
    valid_words = ['a', 're', 'and', 'cat']
    invalid_words = ['qrw', 'trp', 'trpo']
    word_list = valid_words + invalid_words
    valid_subset = get_valid_subset(word_list)
    assert valid_subset == valid_words
    print(valid_words)
    print(valid_subset)

def user_word_query():
    word = input("get plays for word: ")
    possibilities = get_valid_subset(get_naive_perms(word))
    print(possibilities)

def word2word(w1, w2):
    queue = [w1]
    parents = {}
    visited = set()
    while queue:
        queue.sort(key=lambda x:levenshtein(x, w2))
        print(f'queue len: {len(queue)}')
        print(f'{queue[:5]}')
        word = queue[0]
        plays = get_valid_plays(word)
        visited.add(word)
        del queue[0]
        for play in plays:
            if parents.get(play) is None:
                parents[play] = [word]
            else:
                parents[play].append(word)
        if word == w2:
            break
        queue = queue + [play for play in plays if play not in visited]
    return get_parent_path(w1, w2, parents)[::-1]

def get_parent_path(oword, tword, parents):
    path = []
    cword = tword
    while parents.get(cword) is not None:
        print(cword)
        path.append(cword)
        if cword == oword:
            break
        cword = parents[cword][0]
    return path

def menu(options):
    r = input(f"What would you like to do? {options}\n")
    so = sorted(options, key=lambda x:sum(-1 for i in r if i in x))
    return so[0]

def user_word2word():
    w1 = input('word 1:')
    w2 = input('word 2:')

    ok = True
    if w1 not in swords:
        print("Word 1 not in word list")
        ok = False
    if w2 not in swords:
        print("Word 2 not in word list")
        ok = False
    if not ok:
        return
    print(word2word(w1,w2))

while True:
    options = ['query', 'word2word']
    resp = menu(options)
    if resp == 'query':
        user_word_query()
    if resp == 'word2word':
        user_word2word()
print(word2word('worms', 'revolution'))
