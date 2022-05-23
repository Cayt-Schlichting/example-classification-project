from sklearn.metrics import classification_report, accuracy_score, recall_score, precision_score, confusion_matrix, f1_score


def stats_result(p,null_h,**kwargs):
    """
    Compares p value to alpha and outputs whether or not the null hypothesis
    is rejected or if it failed to be rejected.
    DOES NOT HANDLE 1-TAILED T TESTS
    
    Required inputs:  p, null_h (str)
    Optional inputs: alpha (default = .05), chi2, r, t
    
    """
    #get r value if passed, else none
    t=kwargs.get('t',None)
    r=kwargs.get('r',None)
    chi2=kwargs.get('chi2',None)
    alpha=kwargs.get('alpha',.05) #default value of alpha is .05
    print(f'\n\033[1mThe null hypothesis was:\033[0m {null_h}')
    
    if p < alpha: print(f"\033[1mWe reject the null hypothesis\033[0m, p = {p} | α = {alpha}")
    else: print(f"We failed to reject the null hypothesis, p = {p} | α = {alpha}")
    
    if 't' in kwargs: print(f'  t: {t}')
    if 'r' in kwargs: print(f'  r: {r}')
    if 'chi2' in kwargs: print(f'  chi2: {chi2}')

    return None



def print_model_stats(act,mod,pos,**kwargs):
    """
    Gets model statistics.  Only handles binary target variables at the moment.
    Parameters:
      (R) -        act: pandas series of actual target values
      (R) -        mod: pandas series of modeled target values (must be same length as act)
      (R) -        pos: positive outcome for target variable 
      (O) - model_dict: If model dictionary is provided, it updates dictionary with model statistics. 
      (O) -  to_screen: If False, model doesn't print to screen.  Default True
                        
    NOTE:  
    recall = sensitivity = true positive rate
    miss rate = false negative rate
    specificity = true negative rate    
    """
    #Get return df parameter.  Default is false, which returns none and prints the statistics
    ret_df = kwargs.get('ret_df',False)
    model_dict = kwargs.get('model_dict',None)
    to_screen = kwargs.get('to_screen',True)
    
    #Create label list - binary confusion matrix needs positive value last
    #populate rest of list with possible outcomes
    oth=list(act.unique())
    oth.remove(pos)
    labels = oth +[pos]
    
    #run confusion matrix
    cm = confusion_matrix(act,mod,labels=labels)
    
    #If two target variables ravel cm, else break softly 
    if len(labels) == 2: 
        tn, fp, fn, tp = cm.ravel()
    else: #UPDATE THIS TO HANDLE 3+ OUTCOMES
        print('function cannot handle greater than 2 target variable outcomes')
        return None
    
    #Calculate all the model scores
    recall = recall_score(act,mod,pos_label=pos,zero_division=0)
    precision = precision_score(act,mod,pos_label=pos,zero_division=0)
    f1 = f1_score(act,mod,pos_label=pos,zero_division=0)
    acc = accuracy_score(act,mod)
    fnr = fn/(tp+fn)
    fpr = fp/(tn+fp)
    support_pos = tp + fn
    support_neg = fp + tn
    
    ###UPDATE THIS FIRST IF STATEMENT. WE WANT SOME KIND OF SERIES OR DATAFRAME TO PLAY WITH
    #If passed a dictionary, update it:
    # if type(model_dict) == dict:
    #     model_dict[mod.name].update({
    #         "Accuracy": {acc},
    #         "precision": {precision},
    #         "recall": {recall},
    #         "F1": {f1},
    #         "FNR": {fnr},
    #         "FPR": {fpr},
    #         "support_pos":{support_pos},
    #         "support_neg":{support_neg},
    #         "TP": {tp},
    #         "FP": {fp},
    #         "FN": {fn},
    #         "TN": {tn},
    #     })
    #If passed a dictionary, update it:
    if type(model_dict) == dict:
        model_dict[mod.name].update({
            "Accuracy": {acc},
            "precision": {precision},
            "recall": {recall},
            "F1": {f1},
            "FNR": {fnr},
            "FPR": {fpr},
            "support_pos":{support_pos},
            "support_neg":{support_neg},
            "TP": {tp},
            "FP": {fp},
            "FN": {fn},
            "TN": {tn},
        })
    #print to screen unless user told you not to
    if to_screen:
        print(f'\033[1mModel: {mod.name}  Positive: {pos}\033[0m')
        print('\033[4mConfusion Matrix\033[0m')
        print(f'  TP: {tp}   FP: {fp}')
        print(f'  FN: {fn}   TN: {tn}')
        print('\033[4mAdditional Information\033[0m')
        print(f'      Accuracy: {acc:.3f}')
        print(f'     Precision: {precision:.3f}')
        print(f'        Recall: {recall:.3f}')
        print(f'      F1 score: {f1:.3f}')
        print(f'False neg rate: {fnr:.3f}')
        print(f'False pos rate: {fpr:.3f}')   
        print(f' Support (pos): {support_pos}')
        print(f' Support (neg): {support_neg}\n')
    
    return None