import sqlite3


def get_all(num_moves=None, num_trials=None, num_results=float('inf')):
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    # ? Is there  a better way to do this? Something like num_moves = anything?
    # ? That way I can set default values for num_moves and num_trials to be that 'anything'
    # ? and I wouldn't have this if-else
    if num_moves and num_trials:
        cursor.execute("SELECT * FROM results WHERE num_moves = ? AND num_trials = ? ORDER BY highest_score DESC",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT * FROM results ORDER BY highest_score DESC")
    results_done = 0
    for attempt_no, num_moves, num_trials, highest_score, did_win in cursor.fetchall():
        if results_done >= num_results:
            break
        results_done += 1
        print(
            f"""TRIAL #{attempt_no}
        num_moves  = {num_moves}
        num_trials = {num_trials}
        HIGH SCORE = {highest_score}
        WIN: {"yes" if did_win else "no"}
        """
        )
    conn.close()
    return results_done


def get_wins(num_moves=None, num_trials=None, num_results=float('inf')):
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT * FROM results WHERE num_moves = ? AND num_trials = ? AND did_win = 1 ORDER BY highest_score DESC",
                       (num_moves, num_trials))
    else:
        cursor.execute(
            "SELECT * FROM results WHERE did_win = 1 ORDER BY highest_score DESC")
    results_done = 0
    for attempt_no, num_moves, num_trials, highest_score, did_win in cursor.fetchall():
        if results_done >= num_results:
            break
        results_done += 1
        print(
            f"""TRIAL #{attempt_no}
        num_moves  = {num_moves}
        num_trials = {num_trials}
        HIGH SCORE = {highest_score}
        WIN: {"yes" if did_win else "no"}
        """
        )
    conn.close()
    return results_done


def erase_all():
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS results")
    conn.commit()
    conn.close()


def get_win_rate(num_moves=None, num_trials=None):
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT AVG(did_win) FROM results WHERE num_moves = ? AND num_trials = ?",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT AVG(did_win) FROM results")
    win_rate = cursor.fetchone()[0]
    print(f"WIN RATE: {round(win_rate * 100, 2)}%")
    conn.close()


def get_avg_score(num_moves=None, num_trials=None):
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT AVG(highest_score) FROM results WHERE num_moves = ? AND num_trials = ?",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT AVG(highest_score) FROM results")
    avg_score = cursor.fetchone()[0]
    print(f"AVG SCORE: {avg_score}")
    conn.close()
