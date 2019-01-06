""" Provides basic functions for generating and solving bimatrix games.

Functions:
    game:     generates and returns a random bimatrix.
    zerosum:  generates and returns a random bimatrix for a zero sum game.
    pnash:    computes pure Nash equilibria of a bimatrix game.
    ibr:      executes Iterative Best Response on a bimatrix game.
    fictplay: executes Fictitious Play on a bimatrix game.
"""

import random

def game(m, n, maxPayoff = 100):
    """ Generates a mxn matrix of pairs of integers.
    
    Each pair's numbers are determined uniformly at random
    from 1, ..., maxPayoff.

    Args:
        m (int): number of rows (actions of the row player).
        n (int): number of columns (actions of the column player).
        maxPayoff (int): the maximum payoff of either player.

    Returns: a mxn matrix of pairs of random integers.
    """
    paymat = [ n * [ None ] for i in range(m) ]
    for i in range(m):
        for j in range(n):
            paymat[i][j] = (
                    random.randint(1, maxPayoff),
                    random.randint(1, maxPayoff))
    return paymat

def zerosum(m, n, maxPayoff = 100):
    """ Generates a mxn matrix of pairs of integers.
    
    Each pair consists of two integers of opposite sign;
    the absolute value is determined uniformly at random
    from 1, ..., maxPayoff; the negative integer between
    the two is determined uniformly at random.

    Args:
        m (int): number of rows (actions of the row player).
        n (int): number of columns (actions of the column player).
        maxPayoff (int): the maximum payoff of either player.

    Returns: a mxn matrix of pairs of integers with opposite
             sign and randomly chosen absolute value.
    """
    paymat = [ n * [ None ] for i in range(m) ]
    for i in range(m):
        for j in range(n):
            payoff = random.randint(1, maxPayoff)
            if random.randint(0, 1) == 0:
                paymat[i][j] = (payoff, -payoff)
            else:
                paymat[i][j] = (-payoff, payoff)
    return paymat

def pnash(paymat):
    """ Computes the pure Nash Equilibria (if any) of a bimatrix game.

    Args:
        paymat (list of lists): a mxn matrix, represented by a list of
            m lists, each having n elements. Each entry (element) of the
            matrix is a pair (tuple) of payoff values for the players.
            In particular, in an entry '(p, q)': 'p' is the payoff of the
            "row" player and 'q' is the payoff of the "column" player.

    Returns: a list of pairs (tuples) of pure strategies that constitute
             pure Nash equilibria for the bimatrix game defined by the
             argument 'paymat'. Each pair '(r, c)' in the returned list 
             is an equilibrium action profile, wherein the "row" player
             chooses row 'r', while the "column" player chooses the
             column 'c'.

    """

    result = []
    m, n = len(paymat), len(paymat[0])
    cMark = [ n * [ False ] for i in range(m) ]
    # For each action of the row player:
    for i in range(m):
        # Find the best action value of the column player.
        cMaxPayoff = 0
        for payoff in paymat[i]:
            if payoff[1] >= cMaxPayoff:
                cMaxPayoff = payoff[1]
        # Mark the best actions of the columns player.
        for j in range(n):
            if paymat[i][j][1] == cMaxPayoff:
                cMark[i][j] = True
    # For each action of the column player:
    for j in range(n):
        # Find the best action value of the row player.
        rMaxPayoff = 0
        for i in range(m):
            if paymat[i][j][0] >= rMaxPayoff:
                rMaxPayoff = paymat[i][j][0]
        # Find the best actions of the row player.
        # If the coincide with marked actions of the
        # column player, append the profile to the result.
        for i in range(m):
            if paymat[i][j][0] == rMaxPayoff:
                if cMark[i][j] == True:
                    result.append((i, j))
    return result

def ibr(paymat):
    """ Executes Iterative Best Response on a bimatrix game; either it
    converges to a pure Nash Equilibrium of the game, or terminates
    after a number of best responses equal to the number of elements
    in the game's matrix.

    Args:
        paymat (list of lists): a mxn matrix, represented by a list of
            m lists, each having n elements. Each entry (element) of the
            matrix is a pair (tuple) of payoff values for the players.
            In particular, in an entry '(p, q)': 'p' is the payoff of the
            "row" player and 'q' is the payoff of the "column" player.

    Returns: a pair (tuple) of pure strategies that constitute
             pure Nash equilibrium for the bimatrix game defined by the
             argument 'paymat'. Each pair '(r, c)' in the returned list 
             is an equilibrium action profile, wherein the "row" player
             chooses row 'r', while the "column" player chooses the
             column 'c'.

    """
    m = len(paymat)
    n = len(paymat[0])
    profile = (random.randint(0, m-1), random.randint(0, n-1))
    r = profile[0]
    c = profile[1]
    stepCount = 0
    updated = 2
    # While at least one player updates and no
    # more than mxn profiles have been visited.
    while updated > 0 and stepCount < 2 + m*n:
        print(profile)
        updated -= 1
        if stepCount % 2 == 0:
            # Find best response of "Row" player (0)
            rMaxPayoff = paymat[r][c][0]
            for i in range(m):
                if paymat[i][c][0] > rMaxPayoff:
                    r = i
                    rMaxPayoff = paymat[r][c][0]
                    updated = min(updated + 1, 2)
            # Update the profile
            profile = (r, c)
        else:
            # Find best response of "Column" player (1)
            cMaxPayoff = paymat[r][c][1]
            for j in range(n):
                if paymat[r][j][1] > cMaxPayoff:
                    c = j
                    cMaxPayoff = paymat[r][c][1]
                    updated = min(updated + 1, 2)
            # Update the profile
            profile = (r, c)
        stepCount += 1
    return profile

def fictplay(paymat, maxIter = 1000, epsilon = 0.001):
    """ Executes at most a given number of iterations of Fictitious Play
    on a bimatrix game and as long as the absolute (norm) difference
    of successive mixed strategies is larger than a given epsilon. 

    Args:
        paymat (list of lists): a mxn matrix, represented by a list of
            m lists, each having n elements. Each entry (element) of the
            matrix is a pair (tuple) of payoff values for the players.
            In particular, in an entry '(p, q)': 'p' is the payoff of the
            "row" player and 'q' is the payoff of the "column" player.
        maxIter (int): maximum number of iterations, default value = 1000.
        epsilon (float): convergence tolerance, default value = 0.001.

    Returns: a pair (tuple) of lists, each corresponding to a probability
             distribution over the actions of the "row" and "column" player,
             respectively. 
    """

    m = len(paymat)
    n = len(paymat[0])
    rowCounts = [ 0 for j in range(n) ]
    colCounts = [ 0 for i in range(m) ]
    profile = (random.randint(0, m-1), random.randint(0, n-1))
    rowCounts[profile[1]] = 1
    colCounts[profile[0]] = 1
    iterCount = 0
    rowDiff, colDiff = 1, 1
    while iterCount < maxIter and max(rowDiff, colDiff) > epsilon:
        # Pick the best pure action for row player,
        # against the empirical distribution of actions
        # of the column player.
        rowCountsSum = sum(rowCounts)
        rowMaxPayoff, rowChoice = 0, 0
        for i in range(m):
            # Compute the expected payoff of row player
            # when he plays action i, against empirical
            # distribution of actions of column player.
            rowPayoff = 0
            for j in range(n):
                rowPayoff += (rowCounts[j]/rowCountsSum)*paymat[i][j][0]
            if rowPayoff > rowMaxPayoff:
                rowChoice = i
                rowMaxPayoff = rowPayoff

        # Pick the best pure action for column player,
        # against the empirical distribution of actions
        # of the row player.
        colCountsSum = sum(colCounts)
        colMaxPayoff, colChoice = 0, 0
        for j in range(n):
            # Compute the expected payoff of column player
            # when he plays action i, against empirical
            # distribution of actions of row player.
            colPayoff = 0
            for i in range(m):
                colPayoff += (colCounts[i]/colCountsSum)*paymat[i][j][1]
            if colPayoff > colMaxPayoff:
                colChoice = j 
                colMaxPayoff = colPayoff

        # Update the profile and each player's counts
        # with the choice of the other player.
        profile = (rowChoice, colChoice)
        rowDiff = abs(
                rowCounts[colChoice]/rowCountsSum
                -(rowCounts[colChoice]+1)/(rowCountsSum+1))
        colDiff = abs(
                colCounts[rowChoice]/colCountsSum
                -(colCounts[rowChoice]+1)/(colCountsSum+1))
        rowCounts[colChoice] += 1
        colCounts[rowChoice] += 1
        iterCount += 1

    return(
            [colCounts[i]/sum(colCounts) for i in range(m)],
            [rowCounts[j]/sum(rowCounts) for j in range(n)])

