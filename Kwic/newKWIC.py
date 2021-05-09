def kwic_new_implentation(word, sentences):

    # print(sentences)

    wordlist = str(sentences).split()
    ngrams = [wordlist[i:i + 5] for i in range(len(wordlist) - 4)]
    kwicdict = {}
    for n in ngrams:
        if n[2] not in kwicdict:
            kwicdict[n[2]] = [n]
        else:
            kwicdict[n[2]].append(n)


    for key in kwicdict.keys():
        if word in key:
            for val in kwicdict[key]:
                outstring = ' '.join(val[:2]).rjust(50)
                outstring += ' '
                outstring += ' '.join(str(val[2]).center(len(n[2]) + 15))
                outstring += ' '
                outstring += ' '.join(val[3:])
                print(outstring)


if __name__ == "__main__":

    word = 'complex'
    sent ="""In sequential estimation, unless a conjugate complex prior is used, the posterior
    distribution typically becomes more complexity with each added measurement, and
    the Bayes estimator cannot usually be calculated without resorting to complexion numerical methods"""

    kwic_new_implentation(word, sent)

    # kwic_new_implentation(word, sent)
