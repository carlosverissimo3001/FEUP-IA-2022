from formulation import *
import numpy as np

class Solution:
    def __init__(self, team):
        self.team = team
        self.solution = []
        for _ in range (team.n_projects):
            self.solution.append([random.randint(0,1) for _ in range(team.n_members)])
            #self.solution.append([0 for _ in range(team.n_members)])

    def evaluate(self, solution):
        if len(solution) == 0:
            return 0
        
       # print("NEIGHBOUR: ", solution)
        #return (sum(solution[0]) + sum(solution[1]) + sum(solution[2]) + sum(solution[3]))
        
        project_timer = []
        #Initialization
        for i in range(len(solution)):
            project_timer.append(0)

        score = 0               # Score of the completed projects
        unfinished_projects = 0 # Number of unfinished projects
        solution_members = []   # Members that were chosen to test a given project requirements
        penalties = 0           # Score penalties
        
        i = 0         
        while True:
            for i in range(self.team.n_projects):
                project = self.team.projects[i]
                solution_members.clear()

                if project.is_over:
                    continue
                
                for k in range(len(solution[i])):
                    if solution[i][k]:
                        solution_members.append(self.team.members[k])

                # Check if the project meets the requirements to start
                if not project.has_started:
                    #print(project.name, "has not started yet.")
                    penalties += project.check_requirements(i, solution_members)
                    if project.has_started:
                        project_timer[i] += 1
                        unfinished_projects += 1

                # If the project has started increment the timers
                else:
                    project_timer[i] += 1
                    # If the project's duration is over
                    if project_timer[i] == project.duration:
                        #print(project.name, "has ended in day: ", days)
                        project.is_over = True
                        project.has_started = False
                        score += project.score
                        unfinished_projects -= 1

                        #Unlocking members
                        for member in solution_members:
                            if member.working_on == i:
                                member.reset()
            
            # If all projects get completed
            if unfinished_projects == 0:
                break

        self.team.reset()
        #print("Score: ", score, "Penalties: ", penalties, "Total:", score - penalties)
        return score - penalties

    def neighbour1(self, solution):
        """Change the value of one slot"""
        proj = random.randrange(self.team.n_projects)
        collab = random.randrange(self.team.n_members)

        if solution[proj][collab] == 1:
            solution[proj][collab] = 0
        else:
            solution[proj][collab] = 1

        return solution

    def neighbour2(self, solution):
        """Exchange the slots of two slots"""
        size = self.team.n_projects
        collabs_num = self.team.n_members

        proj1 = random.randrange(size)
        proj2 = random.randrange(size)

        collab1 = random.randrange(collabs_num)
        collab2 = random.randrange(collabs_num)


        if solution[proj1][collab1] == 1:
            solution[proj1][collab1] = 0
        else:
            solution[proj1][collab1] = 1


        if solution[proj2][collab2] == 1:
            solution[proj2][collab2] = 0
        else:
            solution[proj2][collab2] = 1

        return solution

    def neighbour3(self, solution):
        """Change a discipline from slot or exchange the slots of two disciplines"""

        if random.choice([True, False]):
            return self.neighbour1(solution)

        else:
            return self.neighbour2(solution)
