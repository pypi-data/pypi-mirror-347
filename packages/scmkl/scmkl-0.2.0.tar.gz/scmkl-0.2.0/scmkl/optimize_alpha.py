import numpy as np
import gc
import tracemalloc

from scmkl.tfidf_normalize import tfidf_normalize
from scmkl.estimate_sigma import estimate_sigma
from scmkl.calculate_z import calculate_z
from scmkl.train_model import train_model
from scmkl.multimodal_processing import multimodal_processing
from scmkl.test import predict


def _multimodal_optimize_alpha(adatas : list, group_size = 1, tfidf = [False, False],
                               alpha_array = np.round(np.linspace(1.9,0.1, 10),2), k = 4,
                               metric = 'AUROC'):
    '''
    Iteratively train a grouplasso model and update alpha to find the parameter yielding the desired sparsity.
    This function is meant to find a good starting point for your model, and the alpha may need further fine tuning.
    Input:
        adatas- a list of AnnData objects where each object is one modality and Z_train and Z_test are calculated
        group_size- Argument describing how the features are grouped. 
            From Celer documentation:
            "groupsint | list of ints | list of lists of ints.
                Partition of features used in the penalty on w. 
                    If an int is passed, groups are contiguous blocks of features, of size groups. 
                    If a list of ints is passed, groups are assumed to be contiguous, group number g being of size groups[g]. 
                    If a list of lists of ints is passed, groups[g] contains the feature indices of the group number g."
            If 1, model will behave identically to Lasso Regression.
        tifidf_list- a boolean mask where tfidf_list[0] and tfidf_list[1] are respective to adata1 and adata2
            If True, tfidf normalization will be applied to the respective adata during cross validation
        starting_alpha- The alpha value to start the search at.
        alpha_array- Numpy array of all alpha values to be tested
        k- number of folds to perform cross validation over
            
    Output:
        sparsity_dict- Dictionary with tested alpha as keys and the number of selected pathways as the values
        alpha- The alpha value yielding the number of selected groups closest to the target.
    '''

    assert isinstance(k, int) and k > 0, 'Must be a positive integer number of folds'

    import warnings 
    warnings.filterwarnings('ignore')

    y = adatas[0].obs['labels'].iloc[adatas[0].uns['train_indices']].to_numpy()
    
    # Splits the labels evenly between folds
    positive_indices = np.where(y == np.unique(y)[0])[0]
    negative_indices = np.setdiff1d(np.arange(len(y)), positive_indices)

    positive_annotations = np.arange(len(positive_indices)) % k
    negative_annotations = np.arange(len(negative_indices)) % k

    metric_array = np.zeros((len(alpha_array), k))

    cv_adatas = []

    for adata in adatas:
        cv_adatas.append(adata[adata.uns['train_indices'],:].copy())

    del adatas
    gc.collect()

    for fold in np.arange(k):
        
        print(f'Fold {fold + 1}:\n Memory Usage: {[mem / 1e9 for mem in tracemalloc.get_traced_memory()]} GB')

        fold_train = np.concatenate((positive_indices[np.where(positive_annotations != fold)[0]], negative_indices[np.where(negative_annotations != fold)[0]]))
        fold_test = np.concatenate((positive_indices[np.where(positive_annotations == fold)[0]], negative_indices[np.where(negative_annotations == fold)[0]]))

        for i in range(len(cv_adatas)):
            cv_adatas[i].uns['train_indices'] = fold_train
            cv_adatas[i].uns['test_indices'] = fold_test

        # Creating dummy names for cv. 
        # #Necessary for interpretability but not for AUROC cv
        dummy_names = [f'adata {i}' for i in range(len(cv_adatas))]

        # Calculate the Z's for each modality independently
        fold_cv_adata = multimodal_processing(adatas = cv_adatas, names = dummy_names, tfidf = tfidf)
        fold_cv_adata.uns['seed_obj'] = cv_adatas[0].uns['seed_obj']

        gc.collect()

        for j, alpha in enumerate(alpha_array):

            fold_cv_adata = train_model(fold_cv_adata, group_size, alpha = alpha)

            _, metrics = predict(fold_cv_adata, metrics = [metric])
            metric_array[j, fold] = metrics[metric]

        del fold_cv_adata
        gc.collect()

    # Take AUROC mean across the k folds and select the alpha resulting in highest AUROC
    alpha_star = alpha_array[np.argmax(np.mean(metric_array, axis = 1))]
    del cv_adatas
    gc.collect()
    
    return alpha_star


def optimize_alpha(adata, group_size = None, tfidf = False, 
                   alpha_array = np.round(np.linspace(1.9,0.1, 10),2), 
                   k = 4, metric = 'AUROC'):
    '''
    Iteratively train a grouplasso model and update alpha to find the 
    parameter yielding best performing sparsity. This function 
    currently only works for binary experiments.

    Parameters
    ----------
    **adata** : *AnnData* | *list[AnnData]*
        > `AnnData`(s) with `'Z_train'` and `'Z_test'` in 
        `adata.uns.keys()`.

    **group_size** : *None* | *int*
        > Argument describing how the features are grouped. If *None*, 
        `2 * adata.uns['D'] will be used. 
        For more information see 
        [celer documentation](https://mathurinm.github.io/celer/generated/celer.GroupLasso.html).

    **tfidf** : *bool* 
        > If `True`, TFIDF normalization will be run at each fold.
    
    **alpha_array** : *np.ndarray*
        > Array of all alpha values to be tested.

    **k** : *int*
        > Number of folds to perform cross validation over.
            
    **metric**: *str*
        > Which metric to use to optimize alpha. Options
        are `'AUROC'`, `'Accuracy'`, `'F1-Score'`, `'Precision'`, and 
        `'Recall'`

    Returns
    -------
    **alpha_star** : *int*
        > The best performing alpha value from cross validation on 
        training data.

    Examples
    --------
    >>> alpha_star = scmkl.optimize_alpha(adata)
    >>> alpha_star
    0.1
    '''

    assert isinstance(k, int) and k > 0, 'Must be a positive integer number of folds'

    import warnings 
    warnings.filterwarnings('ignore')

    if group_size == None:
        group_size = adata.uns['D'] * 2

    if type(adata) == list:
        alpha_star = _multimodal_optimize_alpha(adatas = adata, group_size = group_size, tfidf = tfidf, alpha_array = alpha_array, metric = metric)
        return alpha_star

    y = adata.obs['labels'].iloc[adata.uns['train_indices']].to_numpy()
    
    # Splits the labels evenly between folds
    positive_indices = np.where(y == np.unique(y)[0])[0]
    negative_indices = np.setdiff1d(np.arange(len(y)), positive_indices)

    positive_annotations = np.arange(len(positive_indices)) % k
    negative_annotations = np.arange(len(negative_indices)) % k

    metric_array = np.zeros((len(alpha_array), k))

    gc.collect()

    for fold in np.arange(k):

        cv_adata = adata[adata.uns['train_indices'],:]

        # Create CV train/test indices
        fold_train = np.concatenate((positive_indices[np.where(positive_annotations != fold)[0]], 
                                     negative_indices[np.where(negative_annotations != fold)[0]]))
        fold_test = np.concatenate((positive_indices[np.where(positive_annotations == fold)[0]], 
                                    negative_indices[np.where(negative_annotations == fold)[0]]))

        cv_adata.uns['train_indices'] = fold_train
        cv_adata.uns['test_indices'] = fold_test

        if tfidf:
            cv_adata = tfidf_normalize(cv_adata, binarize= True)

        cv_adata = estimate_sigma(cv_adata, n_features = 200)
        cv_adata = calculate_z(cv_adata, n_features= 5000)

        gc.collect()

        for i, alpha in enumerate(alpha_array):

            cv_adata = train_model(cv_adata, group_size, alpha = alpha)
            _, metrics = predict(cv_adata, metrics = [metric])
            metric_array[i, fold] = metrics[metric]

            gc.collect()

        del cv_adata
        gc.collect()
        
    # Take AUROC mean across the k folds to find alpha yielding highest AUROC
    alpha_star = alpha_array[np.argmax(np.mean(metric_array, axis = 1))]
    gc.collect()
    

    return alpha_star