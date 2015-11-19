    import sys
    
    def levenshteinDistance(s1,s2):
        if len(s1) > len(s2):
            s1,s2 = s2,s1
        distances = range(len(s1) + 1)
        for index2,char2 in enumerate(s2):
            newDistances = [index2+1]
            for index1,char1 in enumerate(s1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1],
                                                 distances[index1+1],
                                                 newDistances[-1])))
            distances = newDistances
        return distances[-1]
    
    def main():
        word = ''
        rep = False
        if len(sys.argv) == 1:
            word = input()
            rep = True
        else:
            word = sys.argv[1]
        dict_words = []
        with open('Dict.txt','r') as f:
            dict_words = [s[:-1] for s in f.readlines()]
        while rep:
            ret = [s for s in dict_words if levenshteinDistance(s, word) == 1]
            print(', '.join(ret))
            print('----------------')
            word = input()
    
    if __name__ == '__main__':
        main()