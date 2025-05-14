import numpy as np
import scipy


def _tfidf(X, mode = 'filter'):
    '''
    Function to use Term Frequency Inverse Document Frequency 
    filtering for atac data to find meaningful features. If input is 
    pandas data frame or scipy sparse array, it will be converted to a 
    numpy array.
    
    Parameters
    ----------
    x : Data matrix of cell x feature.  Must be a Numpy array or Scipy 
        sparse array.
    mode : Argument to determine what to return.  Must be filter or 
           normalize
    
    Returns
    -------
    TFIDF : Output depends on given 'mode' parameter
            'filter' : returns which column sums are non 0 i.e. which 
                       features are significant
            'normalize' : returns TFIDF filtered data matrix of the 
                          same dimensions as x. Returns as scipy 
                          sparse matrix
    '''
    assert mode in ['filter', 'normalize'], ("mode must be 'filter' or "
                                             "'normalize'.")

    if scipy.sparse.issparse(X):
        tf = scipy.sparse.csc_array(X)
        doc_freq = np.array(np.sum(tf > 0, axis=0)).reshape(-1)
    else:
        tf = np.asarray(X)
        doc_freq = np.sum(X > 0, axis=0)

    idf = np.log1p((1 + X.shape[0]) / (1 + doc_freq))
    tfidf = tf * idf

    if mode == 'normalize':
        if scipy.sparse.issparse(tfidf):
            tfidf = scipy.sparse.csc_matrix(tfidf)
        return tfidf
    elif mode == 'filter':
        significant_features = np.where(np.sum(tfidf, axis=0) > 0)[0]
        return significant_features
        
def _tfidf_train_test(X_train, X_test):
    if scipy.sparse.issparse(X_train):
        tf_train = scipy.sparse.csc_array(X_train)
        tf_test = scipy.sparse.csc_array(X_test)
        doc_freq = np.array(np.sum(X_train > 0, axis=0)).reshape(-1)
    else:
        tf_train = X_train
        tf_test = X_test
        doc_freq = np.sum(X_train > 0, axis=0)

    idf = np.log1p((1 + X_train.shape[0]) / (1 + doc_freq))

    tfidf_train = tf_train * idf
    tfidf_test = tf_test * idf

    if scipy.sparse.issparse(tfidf_train):
        tfidf_train = scipy.sparse.csc_matrix(tfidf_train)
        tfidf_test = scipy.sparse.csc_matrix(tfidf_test)
        
    return tfidf_train, tfidf_test


def tfidf_normalize(adata, binarize = False):
    '''
    Function to TFIDF normalize the data in an adata object. If any 
    rows are entirely 0, that row and its metadata will be removed from
    the object.

    Parameters
    ----------
    **adata** : *AnnData* 
        > `adata.X` to be normalized. If `'train_indices'` and 
        `'test_indices'` in `'adata.uns.keys()'`, normalization will be
        done separately for the training and testing data. Otherwise, 
        it will calculate it on the entire dataset.

    **binarize** : *bool* 
        > If `True`, all values in `adata.X` greater than 1 will become 
        1.

    Returns
    -------
    **adata** : *AnnData* 
        > adata with adata.X TFIDF normalized. Will now have the train 
        data stacked on test data, and the indices will be adjusted 
        accordingly.

    Examples
    --------
    >>> adata = scmkl.create_adata(X = data_mat, 
    ...                            feature_names = gene_names, 
    ...                            group_dict = group_dict)
    >>> 
    >>> adata = scmkl.tfidf_normalize(adata)
    '''
    X = adata.X.copy()
    row_sums = np.sum(X, axis = 1)
    assert np.all(row_sums > 0), "TFIDF requires all row sums be positive"

    if binarize:
        X[X > 0] = 1

    if 'train_indices' in adata.uns_keys():

        train_indices = adata.uns['train_indices'].copy()
        test_indices = adata.uns['test_indices'].copy()

        # Calculate the train TFIDF matrix on just the training data so it is 
        # not biased by testing data
        tfidf_train = _tfidf(X[train_indices,:], mode = 'normalize')

        # Calculate the test TFIDF by calculating it on the train and test 
        # data and index the test data
        tfidf_test = _tfidf(X, mode = 'normalize')[test_indices,:]

        # Impossible to add rows back to original location so we need to 
        # stack the matrices to maintain train/test
        if scipy.sparse.issparse(X):
            tfidf_norm = scipy.sparse.vstack((tfidf_train, tfidf_test))
        else:
            tfidf_norm = np.vstack((tfidf_train, tfidf_test))

        # I'm not sure why this reassignment is necessary, but without, the 
        # values will be saved as 0s in adata
        adata.uns['train_indices'] = train_indices
        adata.uns['test_indices'] = test_indices

        combined_indices = np.concatenate((train_indices, test_indices))

        # Anndata indexes by "rownames" not position so we need to rename the 
        # rows to properly index
        adata_index = adata.obs_names[combined_indices].astype(int)
        tfidf_norm = tfidf_norm[np.argsort(adata_index),:]

    else:

        tfidf_norm = _tfidf(X, mode = 'normalize')

    adata.X = tfidf_norm.copy()

    return adata