import numpy as np


class OutputDecision:
    TH1 = 2
    TH2 = 0.5
    k_max = 5

    def __init__(self, ans_size, secore_size):
        self.final_ans = np.zeros(ans_size, dtype=int)
        self.new_credibility_scores = np.zeros(secore_size)
        self.completed = False

    @staticmethod
    def modifiedInference(esitmation, credibility_scores, k_max):
        row_num, column_num = esitmation.shape
        Y = np.zeros((row_num, column_num))
        X = np.zeros((row_num, column_num))
        for i in range(0, row_num):
            for j in range(0, column_num):
                Y[i][j] += credibility_scores[j]
        for k in range(0, k_max):
            Y_new = np.zeros((row_num, column_num))
            X_new = np.zeros((row_num, column_num))
            for i in range(0, row_num):
                for j in range(0, column_num):
                    for j_prime in range(0, column_num):
                        if j_prime == j: continue
                        X_new[i][j] += esitmation[i][j_prime] * 1.0 * Y[i][j_prime]
            for i in range(0, row_num):
                for j in range(0, column_num):
                    for i_prime in range(0, row_num):
                        if i_prime == i: continue
                        Y_new[i][j] += esitmation[i_prime][j] * 1.0 * X_new[i_prime][j]
                    Y_new[i][j] = min(Y_new[i][j], 1.0)
                    Y_new[i][j] = max(Y_new[i][j], 0)
            Y, Y_new = Y_new, Y
            X, X_new = X_new, X

        res = OutputDecision(row_num, column_num)
        for i in range(0, row_num):
            tmp = 0.0
            for j in range(0, column_num):
                tmp += esitmation[i][j] * 1.0 * Y[i][j]
            res.final_ans[i] = np.sign(tmp)
        for j in range(0, column_num):
            tmp = 0.0
            for i in range(0, row_num):
                tmp += Y[i][j]
            res.new_credibility_scores[j] = tmp / row_num
            res.new_credibility_scores[j] = min(res.new_credibility_scores[j], 1.0)
            res.new_credibility_scores[j] = max(res.new_credibility_scores[j], 0)
        return res

    # TH1: least number of students to do annotation
    # TH2: thresold of confidence
    # k_max: number of iterations for calucation
    # A: 2d np array where A[i][j] is the answer of students j for document i
    #   1 for relevant and -1 for irrelevant
    # credibility_scores: 1d np array where credibility_scores[j] is the credbility
    # score for student j, should be in range (0, 1.0)
    @staticmethod
    def Decision(A, credibility_scores, TH1=TH1, TH2=TH2, k_max=k_max):
        row_num, column_num = A.shape
        if column_num < TH1:
            return OutputDecision(0, 0)
        res = OutputDecision.modifiedInference(A, credibility_scores, k_max)
        S_total = np.sum(credibility_scores)
        for i in range(0, row_num):
            if res.final_ans[i] == 0:
                return OutputDecision(0, 0)
            S_correct = 0.0
            for j in range(0, column_num):
                if A[i][j] == res.final_ans[i]:
                    S_correct += credibility_scores[j]
            if S_total * TH2 > S_correct:
                return OutputDecision(0, 0)
        res.completed = True
        # avoid very low value in credibility scores, in which case the student's answer
        # cannot make any contribution for further assignments.
        for j in range(0, len(res.new_credibility_scores)):
            res.new_credibility_scores[j] = max(0.2, res.new_credibility_scores[j])
        return res
