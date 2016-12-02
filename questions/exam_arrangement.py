'''
Question:
    
    We define that an exam would contain 3 questions, and we use a, b and c 
to represent their diffculty levels. These three questions should satisfy 
the following rules:
    1. a <= b <= c;
    2. b - a <= 10;
    3. c - b <= 10.
    
    Now we have totally n questions made out by the examination committee. We 
would use these questions to design out several different exams (every question
should be set into one exam, without redundant). However, because of the rules 
of the exam, some exams may not have enough 3 questions, which needs examination
committee to make out appropriate questions to satisfy the rules.
    Our teachers in committee are exhausted after the exam  works, please help 
them to find out the least extra questions they should think out.

Input:
    There are two lines of the input:
    The first line indicates the questions number n;
    The second line list out the diffculty levels of the questions.

Output:
    Only one line to show the least number of extra questions need designed.

Sample:
    input:
    4
    20 35 23 40
    output:
    2
'''


class Solution:

    def process(self, questions):

        exam = Exam()
        for question in questions: exam.arrangeQuest(question)
        new_quest_count = exam.getNewQuestCount()
    
        return new_quest_count


class Exam:

    def __init__(self):
    	self.new_questions = 0
        self.questions = []
    
    def arrangeQuest(self, question):
    	while not self.addQuestion(question):
            hardest_quest = self.getHardestQuest()
            new_quest = self.newQuestion(hardest_quest)
            self.addQuestion(new_quest)
            
    def addQuestion(self, question):
    	if len(self.questions) == 0:
	    	self.questions.append(question)
        else:
            hardest_quest = self.getHardestQuest()
            if question - hardest_quest > 10: return False
            self.questions.append(question)
        if len(self.questions) == 3: self.questions = []
        return True

    def getHardestQuest(self):
        hardest_quest = self.questions[-1]
        return hardest_quest
    
    def newQuestion(self, base):
    	new_question = base + 10
        self.new_questions += 1
        return new_question

    def getNewQuestCount(self):
        if len(self.questions) == 0:
            return self.new_questions
        else:
            return self.new_questions + 3-len(self.questions)


if __name__ == "__main__":

    q_number = raw_input()
    q_number = int(q_number)

    questions = raw_input()
    questions = [int(question) for question in questions.split(' ')]
    questions.sort()

    solution = Solution()
    extra_questions = solution.process(questions)

    print extra_questions