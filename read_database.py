import sqlite3


def get_all(num_moves=None, num_trials=None, num_results=float('inf'), will_print=True):
    """Prints out all the trials in the database that satisfy the
    given parameters

    Args:
        num_moves (int, optional): The value for num_moves which printed trials must match. Defaults to None.
        num_trials (int, optional): The value for num_trials which printed trials must match. Defaults to None.
        num_results (int, optional): The maximum number of results to print. Defaults to float('inf').
        will_print(bool, optional): Whether or not to print the results into the terminal. Defaults to True

    Returns:
        list(int, int, int, int, int): List of tuples of all the valid results in the database following the format
        (attempt_no, num_moves, num_trials, highest_score, did_win)
    """
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    # ? Is there  a better way to do this? Something like num_moves = anything?
    # ? That way I can set default values for num_moves and num_trials to be that 'anything'
    # ? and I wouldn't have this if-else
    if num_moves and num_trials:
        # TODO: is there a way to put "LIMIT <num_results>" where num_results can still be +inf?
        cursor.execute("SELECT * FROM results WHERE num_moves = ? AND num_trials = ? ORDER BY highest_score DESC",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT * FROM results ORDER BY highest_score DESC")
    results = cursor.fetchall()
    conn.close()
    # Don't trim if num_results is +inf
    if num_results == float('inf'):
        num_results = len(results)
    # Get only the first <num_results> resuts
    results = results[:num_results]
    if will_print:
        for attempt_no, num_moves, num_trials, highest_score, did_win in results:
            print(
                f"""TRIAL #{attempt_no}
            num_moves  = {num_moves}
            num_trials = {num_trials}
            HIGH SCORE = {highest_score}
            WIN: {"yes" if did_win else "no"}
            """
            )
    return results


def get_wins(num_moves=None, num_trials=None, num_results=float('inf'), will_print=True):
    """Prints out all the winning trials in the database that satisfy the
    given parameters

    Args:
        num_moves (int, optional): The value for num_moves which printed trials must match. Defaults to None.
        num_trials (int, optional): The value for num_trials which printed trials must match. Defaults to None.
        num_results (int, optional): The maximum number of results to print. Defaults to float('inf').
        will_print(bool, optional): Whether or not to print the results into the terminal. Defaults to True

    Returns:
        list(int, int, int, int, int): List of tuples of all the valid results in the database following the format
        (attempt_no, num_moves, num_trials, highest_score, did_win)
    """
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT * FROM results WHERE num_moves = ? AND num_trials = ? AND did_win = 1 ORDER BY highest_score DESC",
                       (num_moves, num_trials))
    else:
        cursor.execute(
            "SELECT * FROM results WHERE did_win = 1 ORDER BY highest_score DESC")
    results = cursor.fetchall()
    conn.close()
    # Don't trim if num_results is +inf
    if num_results == float('inf'):
        num_results = len(results)
    results = results[:num_results]
    # Get only the first <num_results> resuts
    if will_print:
        for attempt_no, num_moves, num_trials, highest_score, did_win in results:
            print(
                f"""TRIAL #{attempt_no}
            num_moves  = {num_moves}
            num_trials = {num_trials}
            HIGH SCORE = {highest_score}
            WIN: {"yes" if did_win else "no"}
            """
            )
    return results


def erase_all():
    """Erases all trial data from the database
    """
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS results")
    conn.commit()
    conn.close()


def get_win_rate(num_moves=None, num_trials=None):
    """Get the win rate for a specified configuration of num_moves and num_trials

    Args:
        num_moves (int, optional): The value for num_moves which printed trials must match. Defaults to None.
        num_trials (int, optional): The value for num_trials which printed trials must match. Defaults to None.
    Returns:
        float: The win rate of all the valid trials
    """
    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT AVG(did_win) FROM results WHERE num_moves = ? AND num_trials = ?",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT AVG(did_win) FROM results")
    win_rate = round(cursor.fetchone()[0] * 100, 2)
    print(f"WIN RATE: {win_rate}%")
    conn.close()
    return win_rate


def get_avg_score(num_moves=None, num_trials=None):
    """Get the average score for a specified configuration of num_moves and num_trials

    Args:
        num_moves (int, optional): The value for num_moves which printed trials must match. Defaults to None.
        num_trials (int, optional): The value for num_trials which printed trials must match. Defaults to None.
    Returns:
        float: The average score for all the valid trials
    """

    conn = sqlite3.connect("2048_AI_results.db")
    cursor = conn.cursor()
    if num_moves and num_trials:
        cursor.execute("SELECT AVG(highest_score) FROM results WHERE num_moves = ? AND num_trials = ?",
                       (num_moves, num_trials))
    else:
        cursor.execute("SELECT AVG(highest_score) FROM results")
    avg_score = round(cursor.fetchone()[0], 2)
    print(f"AVG SCORE: {avg_score}")
    conn.close()
    return avg_score


