import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3, min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    Bayesian information criteria: BIC = -2 * logL + p * logN
    where L is the likelihood of the fitted model, p is the number of parameters,
    and N is the number of data points.

    The lower the BIC value the better the model.
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        max_val = math.inf
        best_model = None
        N,d = self.X.shape
        
        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logL = model.score(self.X, self.lengths)
                p = n * (n-1) + (n-1) + 2 * d * n
                bic_score = -2 * logL + p * np.log(N)
                if bic_score < max_val:
                    max_val = bic_score
                    best_model = model
            except:
                pass
            
        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        max_dic_score = None
        best_model = None

        # Selects other words (different than this word)
        other_words = list(self.words)
        other_words.remove(self.this_word)

        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logL = model.score(self.X, self.lengths)
                logsL = []
                
                # For each word (not this word), fits a model and get score
                for word in other_words:
                    x, lengths = self.hwords[word]
                    logsL.append(model.score(x, lengths))
                        
                dic_score = logL - np.average(logsL)

                if max_dic_score is None or max_dic_score < dic_score:
                    max_dic_score = dic_score
                    best_model = model
            except:
                pass

        return best_model
    
class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        best_score = -math.inf
        best_model = None
        
        split_method = KFold(2)
        
        if len(self.sequences) < 2:
            return self.base_model(self.n_constant)
        
        for n in range(self.min_n_components, self.max_n_components + 1):
            scores = []
            for train_idx, test_idx in split_method.split(self.sequences):
                X_train, length_train = combine_sequences(train_idx, self.sequences)
                
                try:
                    model = self.base_model(X_train, length_train)
                    X_test, length_test = combine_sequences(test_idx, self.sequences)
                    scores.append(model.score(X_test, length_test))
                except:
                    pass
                
            if np.mean(scores) > best_score:
                best_score = np.mean(scores)
                best_model = model

        if best_model is None:
            best_model = self.base_model(self.n_constant)

        return best_model