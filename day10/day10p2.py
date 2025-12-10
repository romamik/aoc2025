import os
from math import gcd


class MachineDescr:
    def __init__(self, s: str):
        s = s.strip()
        i = s.index("]")
        j = s.index("{")
        self.buttons = [
            [int(strnum) for strnum in parens[1:-1].split(",")]
            for parens in s[i + 1 : j].split()
        ]

        self.counters = [int(strnum) for strnum in s[j + 1 : -1].split(",")]

    def __repr__(self):
        return f"(buttons:{self.buttons} counters:{self.counters})"


with open(os.path.dirname(__file__) + "/test.txt", "r") as file:
    input = [MachineDescr(line) for line in file]

"""
initially the counters are all zero
pressing a button increments wired counters by one
we want to get counters to given state

we can view this as a set of linear equations:
let's form matrix, such that mat[cnt][btn] = how button btn affects counter cnt (1 or 0)

we want to find such vector p, where p[btn] - number of presses on the button btn such that mat * p == target
where target[cnt] is the desired final state for the counter cnt

each row in the matrix row=mat[cnt] together with target[cnt] forms a linear equation:
sum(row[btn]*p[btn] for each btn) = target[cnt]

we want to solve this set of equations to find p[btn] such that sum(p) is minimal (total number of button presses)

we can modify these equations:
we have remaining equations and modified equations
at each step we select on variable (btn) and move one equation to modified set, 
and modifying the remaining set such that row[btn] == 0 in each equation (so p[btn] is not used in this equation)
for this we select first equation that has nonzero row[btn] and for every other equation that has nonzero row[btn]
we create a new equation by multipling both by row[btn] from other equation and subtracting.

"""


def solve(machine: MachineDescr) -> int:
    num_btn = len(machine.buttons)
    num_cnt = len(machine.counters)

    # each row is equation, first num_btn elements are button coefficients and last element is target value
    # sum(row[btn]*p[btn]) == row[-1]
    mat = [[0] * (num_btn + 1) for _ in range(num_cnt)]

    for cnt, target in enumerate(machine.counters):
        mat[cnt][-1] = target

    for btn, wires in enumerate(machine.buttons):
        for cnt in wires:
            mat[cnt][btn] = 1

    # this will be the reduced matrix
    # it will be of form such that first row can have all non-zero coefficients
    # second row has row[0]==0
    # third row has row[0]==row[1]==0
    # etc until the last row where only some last elements are non zero
    reduced_mat = []

    # try to reduce every button
    for btn in range(num_btn):
        # select row that has row[btn] != 0
        selected = 0
        while selected < len(mat) and mat[selected][btn] == 0:
            selected += 1

        if selected == len(mat):
            # all equations have row[btn] == 0
            # just take any (last) equation and move to reduced mat
            if len(mat) > 0:
                reduced_mat.append(mat.pop())
        else:
            selected_row = mat[selected]
            # for every other equation make row[btn]==0 by combining with first equation
            for row_num, row in enumerate(mat):
                if row_num == selected:
                    continue

                # make row[btn]==0
                a = selected_row[btn]
                b = row[btn]
                for i in range(num_btn+1):
                    row[i] = row[i]*a - selected_row[i]*b

                # normalize the equation
                row_gcd = gcd(*row)
                if row_gcd != 0:
                    if row[-1] < 0:
                        row_gcd *= -1
                    for i in range(len(row)):
                        row[i] //= row_gcd

            # move selected row to reduced_mat
            reduced_mat.append(mat.pop(selected))

    # now we have reduced_mat which is a system len(reduced_mat) equations for num_btn variables
    # we can select num_btn-len(reduced_mat) free variables and check all possible combinations to find the minimal result
    # if there are no free variables we can just calculate the result
    # we always select first btn as free variables

    num_rows = len(reduced_mat)
    def calc_result(free_values: List[int]):
        # we have reduced_mat, 
        # it is guaranteed that at each row it has only last num_btn-row non-zero items
        # if we supply last (num_btn-num_rows) values to the last equation we will get value for one variable
        # then we can go to the previous row, etc.
        num_rows = len(reduced_mat)
        assert(len(free_values) == num_btn-num_rows)
        result = [0]*num_btn
        for i, v in enumerate(free_values):
            result[i + num_rows] = v

        for row_num in range(num_rows-1, -1, -1):
            row = reduced_mat[row_num]
            v = row[-1]
            btn = -2
            for i, v in enumerate(free_values):
                v -= row[btn] * v
                btn -= 1
            result[row_num] = v

        return result

    if num_rows == num_btn:    
        for row in reduced_mat:
            print(row)
        result = calc_result([])
        for row in reduced_mat:
            for btn in range(num_btn):

        print(result)
        print(sum(result))



result = 0
for machine in input:
    print(machine)
    machine_result = solve(machine)
    # print(machine_result)
    # result += machine_result
# print(result)

"""
(buttons:[[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]] counters:[3, 5, 4, 7])
 p0 p1 p2 p3 p4 p5  target
[1, 1, 0, 1, 0, 0, 7] 
[0, 1, 0, 0, 0, 1, 5] 
[0, 0, 1, 1, 1, 0, 4] 
[0, 0, 0, 0, 1, 1, 3]

known result, p=
[1, 3, 0, 3, 1, 2]
 1+ 3 +0 +3 +0 +0==7
 0 +3          +2==5
          3 +1   ==4
             1 +2==3
"""