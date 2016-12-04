'''
Question: String shift

    We define that a new string function, named shift:
        shift('ABCD', 0) = "ABCD"
        shift('ABCD', 1) = "BCDA"
        shift('ABCD', 2) = "CDAB"
    In other words, this function is used to cut left n characters of the string 
and move them to the right. When giving a n-long string, we defined that it could 
have at most n-times shift process. If shift(string, x)=string (0<=x<n), we call
it a match.
    Please find out there are how many matches in shifting a giving string.

Input:
    Input is one-line string, containing only upper-case and lower-case letters.

Output:
    Output only contains one line indicates how many matches of the string.

Sample:
    input:
    byebyebye
    output:
    3

AC: 100%

URL: http://exercise.acmcoder.com/online/online_judge_list?konwledgeId=158
'''


class Solution:

    def process(self, sentence):

        string = String(sentence)
        match = string.countMatch()

        return match

class String:

    def __init__(self, string):
        self.string = string
        self.length = len(self.string)
        self.max_len = 50000

    # for short string
    def shift(self, move):
        return self.string[move:]+self.string[:move]

    # for long string
    def checkShiftMatch(self, move):
        segments = range(0, self.length+1, self.max_len)
        for segment in segments:
            raw_str_seg = self.getSegment(segment)
            shift_str_seg = self.getSegment(segment+move)
            if not raw_str_seg == shift_str_seg: return False
        return True
        
    def getSegment(self, seg_begin):
        seg_end = seg_begin+self.max_len
        if seg_begin >= self.length:
            seg_begin -= self.length
            seg_end -= self.length
        if seg_end > self.length:
            seg_end -= self.length
            return self.string[seg_begin:]+self.string[:seg_end]
        return self.string[seg_begin:seg_end]
        
    def getLeastMoves(self):
        moves = []
        dustbin = set()
        for cand in range(2, self.length+1):
            if self.length % cand: continue
            if cand in dustbin: continue
            moves.append(cand)
            dust = cand * cand
            while dust < self.length:
                dustbin.add(dust)
                dust *= cand
        if self.length >= 1: 
            moves.insert(0, 1)
            moves.append(self.length)
        return moves

    def countMatch(self):
        # for short string
        if self.length <= self.max_len:
            for move in self.getLeastMoves():
                if self.string == self.shift(move):
                    return self.length / move
        # for long string
        else:
            for move in self.getLeastMoves():
                if self.checkShiftMatch(move):
                    return self.length / move
        return 0

if __name__ == "__main__":

    sentence = raw_input()
    solution = Solution()

    match = solution.process(sentence)

    print match