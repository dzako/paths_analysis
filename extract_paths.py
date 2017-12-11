# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:03:18 2017

@author: jcyra
"""

import numpy as np
import os
import pandas as pd
import re


#checkes if a point of a given index is at the end of any path stored in 
#the provided list of paths
def alreadyinpath(idx, current_frame, paths):
    i = 0    
    for j in range( len(paths) ):        
        path = paths[j][0]
        if path[-1] == idx and current_frame == paths[j][2]:
            return i
        i += 1
    return -1

  
###############
#translates string to the corresponding integer index
def ind(string):
    if( string == 'dim' ):
        return 3
    if( string == 'birth' ):
        return 4
    if( string == 'death' ):
        return 5
    if( string == 'b_lyap' ):
        return 6    
    if( string == 'd_lyap' ):
        return 7
    if( string == 'high_b_lyap' ):
        return 8
    if( string == 'high_d_lyap' ):
        return 9
    if( string == 'avg_p_firstpts' ):
        return 10
    if( string == 'avg_p_lastpts' ):
        return 11
    if( string == 'max_p' ):
        return 12
    if( string == 'avg_b' ):
        return 13
    if( string == 'b_x'):
        return 14
    if( string == 'b_y'):
        return 15
    if( string == 'd_x'):
        return 16
    if( string == 'd_y'):
        return 17

def load_paths(matchcvsdir):
    matches_sub = []
    #fills out the list of arrays with data loaded from csvs
    for filen in sorted( os.listdir(matchcvsdir) ):        
        m = re.match('(\d+)_sub.csv', filen)
        cntsub = 0
        if(m):            
            framei = (int)(m.group(1))
            matches_sub_loc = []  
            datasub = pd.read_csv( matchcvsdir + filen )
            for cntsub in range( 0,datasub.shape[0] ):            
                matches_sub_loc.append([ framei, datasub.loc[cntsub, 'idx'], datasub.loc[cntsub, 'dim'], datasub.loc[cntsub, 'birth'], datasub.loc[cntsub, 'death'], datasub.loc[cntsub, 'b_lyap'], datasub.loc[cntsub, 'd_lyap'], datasub.loc[cntsub, 'matchedidx'], datasub.loc[cntsub, 'matchedbirth'], datasub.loc[cntsub, 'matcheddeath'], datasub.loc[cntsub, 'b_x'], datasub.loc[cntsub, 'b_y'], datasub.loc[cntsub, 'd_x'], datasub.loc[cntsub, 'd_y'] ])
            matches_sub_loc = np.asarray(matches_sub_loc)
            matches_sub.append(matches_sub_loc)
    
    LENT = 9
    paths = [] #list of lists (paths) list storing all data associated with paths 
               #(firstframe, lastframe, dim, list of birth vals, list of death vals, list of b_lyap vals, list of d_lyap vals)
    print(len(matches_sub))
    for i in range( 0, len(matches_sub)-1 ):
        print(i)
        firsta = matches_sub[ i ]    
        appind = []
        for row in firsta:
            #row[7] row['matchedidx']
            if( row[7] > -1): #the point stored in the row h.as a match in the next frame            
                ppidx = alreadyinpath( row[1], i, paths)
                if(ppidx > -1):
                    paths[ppidx][0].append( row[7] )
                    appind.append( ppidx )                
                    paths[ppidx][2] = i+1
                    paths[ppidx][ind('birth')].append( row[8])
                    paths[ppidx][ind('death')].append( row[9])
                    paths[ppidx][ind('b_lyap')].append( row[5])
                    paths[ppidx][ind('d_lyap')].append( row[6])
                    paths[ppidx][ind('b_x')].append( row[10])
                    paths[ppidx][ind('b_y')].append( row[11])
                    paths[ppidx][ind('d_x')].append(row[12])
                    paths[ppidx][ind('d_y')].append(row[13])
                else: #create a new path
                    paths.append( [ [ row[1], row[7] ], i, i+1, row[2], [ row[3], row[8] ], [ row[4], row[9] ], [ row[5] ], [ row[6] ], 0, 0, 0, 0, 0, 0, [ row[10] ], [ row[11] ], [ row[12] ], [ row[13] ] ] )
                    appind.append(len(paths)-1)                
       
        diff = np.setxor1d( appind, list(range(len(paths))) )
        
        dele = [ x for x in diff if len(paths[x][0]) <= LENT  ]
        paths = np.delete( paths, dele, 0 ).tolist()    
    return paths
###############
    



#outf = open('paths.txt', 'w+')
#paths = load_paths('g21/matches/')
#
#print(paths)
#for i in range(len(paths)):
#    #computes some statistics of the paths
#    paths[i][ind('high_b_lyap')] = len( [x for x in paths[i][ind('b_lyap')] if x == 0] )
#    paths[i][ind('high_d_lyap')] = len( [x for x in paths[i][ind('d_lyap')] if x == 0] )
#    pathlen = paths[i][2] - paths[i][1]
#    if( (int)(0.05*pathlen) > 0 ):
#        paths[i][ind('avg_p_firstpts')] = np.average( ( np.array(paths[i][ind('death')]) - np.array(paths[i][ind('birth')]) )[0:(int)(0.05*pathlen)] )
#    if( (int)(0.95*pathlen) < pathlen-1 ):
#        paths[i][ind('avg_p_lastpts')] = np.average( ( np.array(paths[i][ind('death')]) - np.array(paths[i][ind('birth')]) )[(int)(0.95*pathlen):pathlen-1] )
#    paths[i][ind('max_p')] = np.max( np.array(paths[i][ind('death')]) - np.array(paths[i][ind('birth')]) )
#    paths[i][ind('avg_b')] = np.average( np.array(paths[i][ind('birth')]) )
#    
#    if( paths[i][ind('high_b_lyap')] > 0 or paths[i][ind('high_d_lyap')] > 0):
#        outf.write((str)(i) + '(' + (str)(paths[i][1]) + ', ' + (str)(paths[i][2]) +'): ' + (str)(paths[i]) + "\n")
#    
#outf.close()

                