from typing import List, Tuple, Optional

# --------- Grundlegende Spiel-Utilities ---------
EMPTY = ' '
MAX_PLAYER = 'X'  # Maximierer
MIN_PLAYER = 'O'  # Minimierer
INF = 10**9

WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
)

def player_to_move(state: str) -> str:
    return MAX_PLAYER if state.count('X') == state.count('O') else MIN_PLAYER

def winner(state: str) -> Optional[str]:
    for a,b,c in WIN_LINES:
        if state[a] != EMPTY and state[a] == state[b] == state[c]:
            return state[a]
    return None

def Terminal_Test(state: str) -> bool:
    return winner(state) is not None or EMPTY not in state

def Utility(state: str) -> int:
    w = winner(state)
    if w is None: return 0
    return 1 if w == MAX_PLAYER else -1

def Successors(state: str) -> List[Tuple[int, str]]:
    p = player_to_move(state)
    res: List[Tuple[int,str]] = []
    for i,ch in enumerate(state):
        if ch == EMPTY:
            s2 = list(state); s2[i] = p
            res.append((i, ''.join(s2)))
    return res

def Successors_ordered(state: str) -> List[Tuple[int, str]]:
    p = player_to_move(state)
    order = [4,0,2,6,8,1,3,5,7]  # Zentrum, Ecken, Kanten
    res: List[Tuple[int,str]] = []
    for i in order:
        if state[i] == EMPTY:
            s2 = list(state); s2[i] = p
            res.append((i, ''.join(s2)))
    return res

# --------- Reiner Minimax (Knotenzähler) ---------
minimax_nodes = {"max": 0, "min": 0}

def Max_Value_plain(state: str) -> int:
    minimax_nodes["max"] += 1
    if Terminal_Test(state): return Utility(state)
    v = -INF
    for _, s in Successors(state):
        v = max(v, Min_Value_plain(s))
    return v

def Min_Value_plain(state: str) -> int:
    minimax_nodes["min"] += 1
    if Terminal_Test(state): return Utility(state)
    v = +INF
    for _, s in Successors(state):
        v = min(v, Max_Value_plain(s))
    return v

def Minimax_plain(state: str) -> Optional[int]:
    if Terminal_Test(state): return None
    p = player_to_move(state)
    if p == 'X':
        best, act = -INF, None
        for a,s in Successors(state):
            v = Min_Value_plain(s)
            if v >= best: best, act = v, a
        return act
    else:
        best, act = +INF, None
        for a,s in Successors(state):
            v = Max_Value_plain(s)
            if v <= best: best, act = v, a
        return act

# --------- Minimax + Alpha-Beta (Knotenzähler) ---------
alphabeta_nodes = {"max": 0, "min": 0}

def Max_Value_ab(state: str, alpha: int, beta: int, use_ordered=False) -> int:
    alphabeta_nodes["max"] += 1
    if Terminal_Test(state): return Utility(state)
    v = -INF
    succ = Successors_ordered(state) if use_ordered else Successors(state)
    for _, s in succ:
        v = max(v, Min_Value_ab(s, alpha, beta, use_ordered))
        alpha = max(alpha, v)
        if alpha >= beta: break
    return v

def Min_Value_ab(state: str, alpha: int, beta: int, use_ordered=False) -> int:
    alphabeta_nodes["min"] += 1
    if Terminal_Test(state): return Utility(state)
    v = +INF
    succ = Successors_ordered(state) if use_ordered else Successors(state)
    for _, s in succ:
        v = min(v, Max_Value_ab(s, alpha, beta, use_ordered))
        beta = min(beta, v)
        if alpha >= beta: break
    return v

def Minimax_ab(state: str, use_ordered=False) -> Optional[int]:
    if Terminal_Test(state): return None
    p = player_to_move(state)
    alpha, beta = -INF, +INF
    if p == 'X':
        best, act = -INF, None
        succ = Successors_ordered(state) if use_ordered else Successors(state)
        for a,s in succ:
            v = Min_Value_ab(s, alpha, beta, use_ordered)
            if v >= best: best, act = v, a
            alpha = max(alpha, best)
        return act
    else:
        best, act = +INF, None
        succ = Successors_ordered(state) if use_ordered else Successors(state)
        for a,s in succ:
            v = Max_Value_ab(s, alpha, beta, use_ordered)
            if v <= best: best, act = v, a
            beta = min(beta, best)
        return act

# --------- Vergleichsfunktion ---------
def compare_scenarios():
    start = ' ' * 9
    mid = (
        'X' 'O' 'X'
        ' ' 'X' ' '
        'O' ' ' ' '
    )
    for name, state, use_order in [
        ("Start (unord.)", start, False),
        ("Start (geordnet)", start, True),
        ("Mittelspiel (unord.)", mid, False),
        ("Mittelspiel (geordnet)", mid, True),
    ]:
        minimax_nodes["max"] = minimax_nodes["min"] = 0
        _ = Minimax_plain(state)
        plain_total = minimax_nodes["max"] + minimax_nodes["min"]

        alphabeta_nodes["max"] = alphabeta_nodes["min"] = 0
        _ = Minimax_ab(state, use_ordered=use_order)
        ab_total = alphabeta_nodes["max"] + alphabeta_nodes["min"]

        print(f"{name}: Minimax={plain_total:5d}, Alpha-Beta={ab_total:5d}, "
              f"Reduktion={(1 - ab_total/max(1,plain_total))*100:5.1f}%")

# ---- Hauptaufruf ----
if __name__ == "__main__":
    compare_scenarios()