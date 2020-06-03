'''
Use of this function needs pandas, stats (from scipy) and numpy imports
'''
def minimize_skew_with_transform(df, np, pd, stats, SKEW_CUT_OFF=[-1,1]):
    '''
    Finds columns with excess skew and minimizes them the best way possible by checking the best transform to use
    Transforms include: log, sqrt, boxcox
    
    df: dataframe to have transforms
    stats: stats from scipy needed for boxcox transform
    np: numpy reference for func
    
    General rule of thumb for skew cut off value us [-1, 1] but can be changed
    
    returns dataframe with changed values, and dictionary with changes in skew for each col
    '''
    
    skews_df = pd.DataFrame(df.skew())
    columns_with_high_skew = list()
    
    #get list of skewed data
    for col in skews_df.T.columns:
        skew_score = skews_df.T[col].values[0]
        if skew_score < SKEW_CUT_OFF[0] or skew_score > SKEW_CUT_OFF[1]:
            columns_with_high_skew.append(col)
    
    print('High skew columns: {}\n'.format(', '.join(columns_with_high_skew)))
    
    diff = {}
    #find best transform for column and apply it to original df
    for col in columns_with_high_skew:
        
        col_skew = skews_df.T[col].values[0]
        #Pre-set them higher for when we look for minimal val
        l_trans = col_skew + 1
        sqrt_trans = col_skew + 1
        box_cox_trans = col_skew + 1
        NO_ZEROS = False
        if 0 not in df[col].values:
            NO_ZEROS = True
        if np.min(df[col]) >= 0:
            sqrt_trans = np.sqrt(df[col]).skew()
            if NO_ZEROS:                
                l_trans = np.log(df[col]).skew()
                box_cox_trans = pd.Series(stats.boxcox(df[col])[0]).skew()
       
        
        #order important for next case statement
        max_vals = [l_trans, sqrt_trans, box_cox_trans, col_skew]
        
        ind = np.argmin(max_vals)        
        if ind == 0:
            print('Log transformed: {}'.format(col))
            diff[col] = (col_skew - l_trans)
            df[col] = np.log(df[col])
        elif ind == 1:
            print('Sqrt transformed: {}'.format(col))
            diff[col] = (col_skew - sqrt_trans)
            df[col] == np.sqrt(df[col])
        elif ind == 2:
            print('Boxcox transformed: {}'.format(col))
            diff[col] = (col_skew - box_cox_trans)
            df[col] == pd.Series(stats.boxcox(df[col])[0])
        else:
            diff[col] = 0.0
            #no change as the original value is least skew when unchanged
            
            
    print('Skew minimization complete')
    return (df, diff)
        