from local_games.base import LocalArena
from itertools import permutations
import numpy as np
from collections import defaultdict


class LemonadeArena(LocalArena):
    def __init__(self, num_rounds=1000, players=[], timeout=1, handin=False):
        super().__init__(num_rounds, players, timeout, handin)
        self.game_name = "Lemonade Stand"
        self.valid_actions = list(range(0, 12))

        if not self.handin_mode:
            assert len(self.players) >= 3, "Arena must have at least 3 players"

        for idx in range(len(self.players)):
            if self.handin_mode:
                try:
                    player = self.players[idx]
                    self.game_reports[player.name] = {
                        "action_history": [],
                        "util_history": [],
                        "index": idx,
                        "timeout_count": 0,
                        "global_timeout_count": 0,
                        "disconnected": False
                    }
                except:
                    continue
            else:
                player = self.players[idx]
                self.game_reports[player.name] = {
                    "action_history": [],
                    "util_history": [],
                    "index": idx,
                    "global_timeout_count": 0
                }

        self.results = []
        self.game_num = 1

    def reset_game_reports(self):
        for player in self.players:
            if self.handin_mode:
                try:
                    self.game_reports[player.name]["action_history"] = []
                    self.game_reports[player.name]["util_history"] = []
                except:
                    continue
            else:
                self.game_reports[player.name]["action_history"] = []
                self.game_reports[player.name]["util_history"] = []

    def run(self):
        for p1, p2, p3 in permutations(self.players, 3):
            if self.handin_mode:
                if self.game_reports[p1.name]['disconnected'] or self.game_reports[p2.name]['disconnected'] or self.game_reports[p3.name]['disconnected']:
                    continue
                else:
                    try:
                        self.run_func_w_time(
                            p1.setup, self.timeout, p1.name)
                    except:
                        self.game_reports[p1.name]['disconnected'] = True
                        continue

                    try:
                        self.run_func_w_time(
                            p2.setup, self.timeout, p2.name)
                    except:
                        self.game_reports[p2.name]['disconnected'] = True
                        continue

                    try:
                        self.run_func_w_time(
                            p3.setup, self.timeout, p3.name)
                    except:
                        self.game_reports[p3.name]['disconnected'] = True
                        continue

                    try:
                        self.run_game(p1, p2, p3)
                    except:
                        self.reset_game_reports()
                        continue
            else:
                self.run_func_w_time(p1.setup, self.timeout, p1.name)
                self.run_func_w_time(p2.setup, self.timeout, p2.name)
                self.run_func_w_time(p3.setup, self.timeout, p3.name)
                self.run_game(p1, p2, p3)
        results = self.summarize_results()
        return results

    def calculate_utils(self, p1_action, p2_action, p3_action):
        if p1_action not in self.valid_actions and p2_action not in self.valid_actions and p3_action not in self.valid_actions:
            utils = [0, 0, 0]
        elif p1_action not in self.valid_actions and p2_action not in self.valid_actions:
            utils = [0, 0, 24]
        elif p1_action not in self.valid_actions and p3_action not in self.valid_actions:
            utils = [0, 24, 0]
        elif p2_action not in self.valid_actions and p3_action not in self.valid_actions:
            utils = [24, 0, 0]
        elif p1_action not in self.valid_actions:
            utils = [0, 12, 12]
        elif p2_action not in self.valid_actions:
            utils = [12, 0, 12]
        elif p3_action not in self.valid_actions:
            utils = [12, 12, 0]
        elif p1_action == p2_action and p2_action == p3_action:
            utils = [8, 8, 8]
        elif p1_action == p2_action:
            utils = [6, 6, 12]
        elif p1_action == p3_action:
            utils = [6, 12, 6]
        elif p2_action == p3_action:
            utils = [12, 6, 6]
        else:
            utils = [0, 0, 0]
            actions = [p1_action, p2_action, p3_action]
            sorted_actions = sorted(actions)
            index_map = {action: index for index,
                         action in enumerate(actions)}
            sorted_indices = [index_map[action]
                              for action in sorted_actions]
            u1 = sorted_actions[1] - sorted_actions[0]
            u2 = sorted_actions[2] - sorted_actions[1]
            u3 = 12 + sorted_actions[0] - sorted_actions[2]
            utils[sorted_indices[0]] = u1 + u3
            utils[sorted_indices[1]] = u1 + u2
            utils[sorted_indices[2]] = u2 + u3
        return utils

    def run_game(self, p1, p2, p3):
        for _ in range(self.num_rounds):
            if self.handin_mode:
                if self.game_reports[p1.name]['timeout_count'] < self.timeout_tolerance:
                    try:
                        p1_action = self.run_func_w_time(
                            p1.get_action, self.timeout, p1.name, -1)
                    except:
                        self.game_reports[p1.name]['disconnected'] = True
                        p1_action = -1
                else:
                    self.game_reports[p1.name]['disconnected'] = True
                    p1_action = -1

                if self.game_reports[p2.name]['timeout_count'] < self.timeout_tolerance:
                    try:
                        p2_action = self.run_func_w_time(
                            p2.get_action, self.timeout, p2.name, -1)
                    except:
                        self.game_reports[p2.name]['disconnected'] = True
                        p2_action = -1
                else:
                    self.game_reports[p2.name]['disconnected'] = True
                    p2_action = -1

                if self.game_reports[p3.name]['timeout_count'] < self.timeout_tolerance:
                    try:
                        p3_action = self.run_func_w_time(
                            p3.get_action, self.timeout, p3.name, -1)
                    except:
                        self.game_reports[p3.name]['disconnected'] = True
                        p3_action = -1
                else:
                    self.game_reports[p3.name]['disconnected'] = True
                    p3_action = -1

            else:
                p1_action = self.run_func_w_time(
                    p1.get_action, self.timeout, p1.name, -1)
                p2_action = self.run_func_w_time(
                    p2.get_action, self.timeout, p2.name, -1)
                p3_action = self.run_func_w_time(
                    p3.get_action, self.timeout, p3.name, -1)

            self.game_reports[p1.name]['action_history'].append(p1_action)
            self.game_reports[p2.name]['action_history'].append(p2_action)
            self.game_reports[p3.name]['action_history'].append(p3_action)

            p1_util, p2_util, p3_util = self.calculate_utils(
                p1_action, p2_action, p3_action)
            self.game_reports[p1.name]['util_history'].append(p1_util)
            self.game_reports[p2.name]['util_history'].append(p2_util)
            self.game_reports[p3.name]['util_history'].append(p3_util)

            p1.game_history['my_action_history'].append(p1_action)
            p1.game_history['my_utils_history'].append(p1_util)
            p1.game_history['opp1_action_history'].append(p2_action)
            p1.game_history['opp1_utils_history'].append(p2_util)
            p1.game_history['opp2_action_history'].append(p3_action)
            p1.game_history['opp2_utils_history'].append(p3_util)

            p2.game_history['my_action_history'].append(p2_action)
            p2.game_history['my_utils_history'].append(p2_util)
            p2.game_history['opp1_action_history'].append(p1_action)
            p2.game_history['opp1_utils_history'].append(p1_util)
            p2.game_history['opp2_action_history'].append(p3_action)
            p2.game_history['opp2_utils_history'].append(p3_util)

            p3.game_history['my_action_history'].append(p3_action)
            p3.game_history['my_utils_history'].append(p3_util)
            p3.game_history['opp1_action_history'].append(p1_action)
            p3.game_history['opp1_utils_history'].append(p1_util)
            p3.game_history['opp2_action_history'].append(p2_action)
            p3.game_history['opp2_utils_history'].append(p2_util)

            if self.handin_mode:
                try:
                    self.run_func_w_time(p1.update, self.timeout, p1.name)
                except:
                    self.game_reports[p1.name]['disconnected'] = True

                try:
                    self.run_func_w_time(p2.update, self.timeout, p2.name)
                except:
                    self.game_reports[p2.name]['disconnected'] = True

                try:
                    self.run_func_w_time(p3.update, self.timeout, p3.name)
                except:
                    self.game_reports[p3.name]['disconnected'] = True
            else:
                self.run_func_w_time(p1.update, self.timeout, p1.name)
                self.run_func_w_time(p2.update, self.timeout, p2.name)
                self.run_func_w_time(p3.update, self.timeout, p3.name)

        print(f"Game {self.game_num}:")
        p1_tot_util = self.print_results(p1)
        p2_tot_util = self.print_results(p2)
        p3_tot_util = self.print_results(p3)
        agents = [p1, p2, p3]
        total_u = [p1_tot_util, p2_tot_util, p3_tot_util]
        winner = agents[np.argmax(total_u)].name
        self.results.append(
            [p1.name, p2.name, p3.name, p1_tot_util, p2_tot_util, p3_tot_util, winner])
        self.game_num += 1
        self.reset_game_reports()

    def print_results(self, p):
        action_counts = [0 for _ in range(len(self.valid_actions) + 1)]
        for action in self.game_reports[p.name]['action_history']:
            if action in self.valid_actions:
                action_counts[action] += 1
            else:
                action_counts[len(self.valid_actions)] += 1
        print_smt = f"{p.name} set up their Lemonade Stand at"
        for i in range(len(self.valid_actions) - 1):
            print_smt += f" Location {i} {action_counts[i]} times,"
        print_smt += f" and Location {len(self.valid_actions) - 1} {action_counts[len(self.valid_actions) - 1]} times."
        if not self.handin_mode:
            print(print_smt)
            if action_counts[len(self.valid_actions)] > 0:
                print(
                    f"{p.name} submitted {action_counts[len(self.valid_actions)]} invalid moves")
            if self.game_reports[p.name]['global_timeout_count'] > 0:
                print(
                    f"{p.name} timed out {self.game_reports[p.name]['global_timeout_count']} times")
                self.game_reports[p.name]['global_timeout_count'] = 0

        total_util = sum(self.game_reports[p.name]['util_history'])

        avg_util = total_util / \
            len(self.game_reports[p.name]['util_history'])
        if not self.handin_mode:
            print(
                f"{p.name} got a total utility of {total_util} and a average utility of {avg_util}")
        return total_util

    def summarize_results(self):
        import pandas as pd
        df = pd.DataFrame(self.results)
        df.columns = ['Agent 1', 'Agent 2', 'Agent 3',
                      'Agent 1 Score', 'Agent 2 Score', 'Agent 3 Score', 'Winner']
        print(f"Extended Results: \n {df}")

        total_util_dict = defaultdict(lambda: [0, 0])
        for p1, p2, p3, p1_util, p2_util, p3_util, _ in self.results:
            total_util_dict[p1][0] += p1_util
            total_util_dict[p2][0] += p2_util
            total_util_dict[p3][0] += p3_util
            total_util_dict[p1][1] += 1
            total_util_dict[p2][1] += 1
            total_util_dict[p3][1] += 1

        res_summary = []
        for key, value in total_util_dict.items():
            if self.handin_mode and self.game_reports[key]['disconnected']:
                res_summary.append([key, float('-inf'), float('-inf')])
            elif value[1] > 0:
                res_summary.append(
                    [key, value[0] / value[1], value[0] / (value[1] * self.num_rounds)])
            else:
                res_summary.append([key, 0, 0])

        sum_df = pd.DataFrame(res_summary)
        sum_df.columns = ['Agent Name', 'Average Utility', 'Final Score']
        sum_df = sum_df.sort_values('Final Score', ascending=False)
        sum_df['Final Score'] = sum_df['Final Score'].replace(float('-inf'), 'DISCONNECTED')
        print(f"Results: \n {sum_df}")
        return sum_df
