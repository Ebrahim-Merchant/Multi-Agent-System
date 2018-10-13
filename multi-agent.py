import csv
import os
import random
import statistics as stats
import pygame
from Agent import Agent
from Target import Target

'''
	The function draw a move of agents and targets on the screen.
	The function takes into account that agents should not be faced
'''


def move(agents, targets):
    for i in range(len(agents)):
        if (agents[i].get_target() is not None):
            temp_x = agents[i].get_target().get_x() - agents[i].get_x()
            if (temp_x > 0):
                x = k * (-1) ** 2
            else:
                x = k * (-1) ** 1

            temp_y = agents[i].get_target().get_y() - agents[i].get_y()
            if (temp_y > 0):
                y = k * (-1) ** 2
            else:
                y = k * (-1) ** 1
        else:
            x = k * (-1) ** random.randint(1, 2)
            y = k * (-1) ** random.randint(1, 2)

        condition1 = ((agents[i].get_x() + x) in range(1, k * 100)) and ((agents[i].get_y() + y) in range(1, k * 100))
        condition2 = True  # Collison Check
        for j in range(len(agents)):
            if i != j and agents[i].get_x() == agents[j].get_x() and agents[i].get_y() == agents[j].get_y():
                condition2 = False
                break
        condition = condition1 and condition2
        while not condition: #if both conditions are not meet then it randomly geneates one
            x = k * (-1) ** random.randint(1, 2)
            y = k * (-1) ** random.randint(1, 2)
            condition1 = ((agents[i].get_x() + x) in range(1, k * 100)) and (
                    (agents[i].get_y() + y) in range(1, k * 100))
            condition2 = True
            for j in range(len(agents)):
                if i != j and agents[i].get_x() == agents[j].get_x() and agents[i].get_y() == agents[j].get_y():
                    condition2 = False
                    break
            condition = condition1 and condition2
        # sets the new position of the agent
        agents[i].put_x(x)
        agents[i].put_y(y)


#function deletes the targets one its in the scope of the radar
def collect_targets(agents, targets):
    for i in range(len(agents)):
        # create a list of target indexes that are determined by the radar
        del_list = []
        n = len(targets[i])
        for j in range(n):
            if (agents[i].get_x() - targets[i][j].get_x()) ** 2 + (
                    agents[i].get_y() - targets[i][j].get_y()) ** 2 <= k ** 2 * 100:
                del_list.append(j)
        del_list = sorted(del_list)
        del_list.reverse()
        for x in del_list:
            agents[i].remove_target(targets[i][x])
            targets[i].pop(x)



#fuction checks if we have meet our goal for scenarios 1, 3 for one agent or all agents in scenario 2
def goal(agents, targets, scenario):
    if scenario == '1' or scenario == '3':
        for i in range(len(agents)):

            if targets[i] == []:
                return True

    if scenario == '2':
        for i in range(len(agents)):
            if targets[i] != []:
                return False
        return True

    return False


def results(agents, targets, scenario, step):
    happiness = []
    agent_comp_array = []
    mycwd = os.getcwd()
    os.chdir("..")
    if not os.path.exists(os.getcwd() + "\\Results"):
        os.makedirs("Results")
        os.chdir(os.getcwd() + "\\Results")
    else:
        os.chdir(os.getcwd() + "\\Results")

    if (os.path.isfile(os.getcwd() + "\\G6_1.csv")):
        file = open("G6_1.csv", "a", newline='')
        writer = csv.writer(file)
        for i in range(0, len(agents)):
            targets_col = 5 - len(targets[i])
            happiness.append(targets_col / (agents[i].count_iter + 1))
        for x in range(0, len(happiness)):
            targets_col = 5 - len(targets[x])
            agent_comp = (happiness[x] - min(happiness)) / (max(happiness) - min(happiness))
            agent_comp_array.append(agent_comp)
            writer.writerow([scenario, agents[x].count_iter, agents[x].name, targets_col, step,
                             happiness[x], max(happiness), min(happiness),
                             (sum(happiness) / len(happiness)), stats.stdev(happiness), agent_comp])
    else:
        file = open("G6_1.csv", "w", newline='')
        writer = csv.writer(file)
        writer.writerow(
            ["Scenario Number",
             "Iteration Number",
             "Agent Number",
             "Number of collected targets",
             "Number of Steps", "Agent Happiness",
             "Maximum Happiness", "Minumum Happiness",
             "Average Happiness",
             "Standard Deviation",
             "Agent Competitiveness"
             ]
        )
        for i in range(0, len(agents)):
            targets_col = 5 - len(targets[i])
            happiness.append(targets_col / (agents[i].count_iter + 1))
        for x in range(0, len(happiness)):
            targets_col = 5 - len(targets[x])
            agent_comp = (happiness[x] - min(happiness)) / (max(happiness) - min(happiness))
            agent_comp_array.append(agent_comp)
            writer.writerow([scenario, agents[x].count_iter, agents[x].name, targets_col, step,
                             happiness[x], max(happiness), min(happiness),
                             (sum(happiness) / len(happiness)), stats.stdev(happiness), agent_comp])
    file.close()
    if (os.path.isfile(os.getcwd() + "\\G6_2.csv")):
        file = open("G6_2.csv", "a", newline='')
        writer = csv.writer(file)
        writer.writerow([scenario, sum(happiness) / len(happiness), sum(agent_comp_array) / len(agent_comp_array)])
    else:
        file = open("G6_2.csv", "w", newline='')
        writer = csv.writer(file)
        writer.writerow(["Scenario", "Average happiness", "Average Agent Competitiveness"])
        writer.writerow([scenario, sum(happiness) / len(happiness), sum(agent_comp_array) / len(agent_comp_array)])

    file.close()
    os.chdir(mycwd)


def main(scenario):
    scenario = input("Please input Scenario (1,2 or 3): ")
    while scenario not in [1, 2, 3, '1', '2', '3']:
        scenario = input("Input error! Input Scenario (1,2 or 3): ")

    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (255, 0, 255)
    RED = (255, 0, 0)
    BLUE = (0, 255, 255)

    # to draw a radar or not
    radar = True

    colors = [WHITE, RED, GREEN, BLUE, YELLOW]
    names = ["Agent A: WHITE", "Agent B: RED", "Agent C: GREEN", "Agent D: BLUE", "Agent E: YELLOW"]

    # create agents and targets with random coordinates
    agents = []
    targets = []
    happiness = [[], [], [], [], []]
    for i in range(5):
        agent = Agent
        agents.append(Agent(random.randint(1, k * 100), random.randint(1, k * 100), names[i], colors[i]))

    for i in range(5):
        target = []
        for j in range(5):
            target.append(
                Target(random.randint(1, k * 100), random.randint(1, k * 100), names[i] + str(j + 1), colors[i]))
        targets.append(target)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (k * 100 + 300, k * 100)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Multi-Agent System, Scenario : " + scenario)

    # Loop until the user clicks the close button.
    done = False

    step = 0
    clock = pygame.time.Clock()

    while not done:
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Set the UI Elements
        # set background
        screen.fill(BLACK)
        # creates agents and targets
        for i in range(5):
            agents[i].draw(screen, radar)
        for i in range(len(targets)):
            for j in range(len(targets[i])):
                targets[i][j].draw(screen)
        # sets the movement of the agents and updates the UI to new x,y coordinates
        move(agents, targets)
        pygame.draw.rect(screen, (100, 100, 100), [k * 100, 0, 300, k * 100], 0)
        # public and private channels
        if scenario == '1':
            for i in range(len(agents)):
                for j in range(len(agents)):
                    for m in range(len(targets[j])):
                        if (agents[i].get_x() - targets[j][m].get_x()) ** 2 + (
                                agents[i].get_y() - targets[j][m].get_y()) ** 2 <= k ** 2 * 100:
                            font = pygame.font.SysFont('Calibri', 15, True, False)
                            text = font.render(agents[i].name[:7] + " locates a target of " + agents[j].name[:7], True,
                                               agents[i].color)
                            screen.blit(text, [k * 100 + 25, 50 * i + 10])

        if scenario == '3':
            for i in range(len(agents)):
                for j in range(len(agents)):
                    for m in range(len(targets[j])):
                        if (agents[i].get_x() - targets[j][m].get_x()) ** 2 + (
                                agents[i].get_y() - targets[j][m].get_y()) ** 2 <= k ** 2 * 100:
                            font = pygame.font.SysFont('Calibri', 15, True, False)
                            text = font.render(agents[i].name[:7] + " locates a target of " + agents[j].name[:7], True,
                                               agents[i].color)
                            if agents[j].name in targets[j][m].name:
                                agents[j].set_target(targets[j][m])
                            screen.blit(text, [k * 100 + 25, 50 * i + 10])

        if scenario == '2':
            for i in range(len(agents)):
                for j in range(len(agents)):
                    for m in range(len(targets[j])):
                        if (agents[i].get_x() - targets[j][m].get_x()) ** 2 + (
                                agents[i].get_y() - targets[j][m].get_y()) ** 2 <= k ** 2 * 100:
                            font = pygame.font.SysFont('Calibri', 15, True, False)
                            text = font.render(
                                agents[i].name[:7] + " to " + agents[j].name[:7] + ": I found your target", True,
                                agents[i].color)
                            if bool(random.getrandbits(1)):
                                    agents[j].set_target(targets[j][m])
                            screen.blit(text, [k * 100 + 25, 50 * i + 10])

        # collect targets that fall within the scope of the radar
        collect_targets(agents, targets)

        # check the condition for the game to end
        if goal(agents, targets, scenario):
            # writer.writerow()
            done = True
        # count the number of iterations for each agent
        if scenario == '1' or scenario == '3':
            for i in range(len(agents)):
                agents[i].count_iter = step + 1
        else:
            for i in range(len(agents)):
                if agents[i].count_iter == 0 and targets[i] == []:
                    agents[i].count_iter = step + 1

        # this is for blinking the radar border
        radar = not radar

        # Update the screen to bring out what we drew
        pygame.display.flip()

        # count the number of iterations
        step += 1
        # limit to r0 frames per second
        clock.tick(30)

    # Close the window and quit.
    pygame.quit()

    # print the result of game
    results(agents, targets, scenario, step)


if __name__ == "__main__":
    k = 8  # scale
    main()

