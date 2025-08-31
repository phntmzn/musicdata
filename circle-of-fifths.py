import pygame, math, time

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

CIRCLE_NOTES = ["C","G","D","A","E","B","F#","C#","G#","D#","A#","F"]
progressions = [
    ["F#m","G#dim","F#"],
    ["D","G#dim","F#m"],
    ["D","G#dim","C#m"],
    ["D","G#dim","Bm"],
    ["A","G#dim","C#m"],
]

def chord_root(c):
    root = c[0]
    if len(c) > 1 and c[1] in "#b":
        root += c[1]
    return root

positions = {}
cx, cy, r = 300, 300, 200
for i, n in enumerate(CIRCLE_NOTES):
    ang = -2*math.pi*i/12 + math.pi/2
    positions[n] = (cx + r*math.cos(ang), cy + r*math.sin(ang))

font = pygame.font.SysFont(None, 30)

running = True
all_lines = []  # keep all drawn connections here

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for prog in progressions:
        prev_pos = None
        for chord in prog:
            root = chord_root(chord)

            # if there is a previous chord, save the connection
            if prev_pos and root in positions:
                all_lines.append((prev_pos, positions[root]))

            screen.fill((0,0,0))

            # draw circle
            pygame.draw.circle(screen, (200,200,200), (cx,cy), r, 1)

            # draw labels
            for n,(x,y) in positions.items():
                col = (255,255,0) if n==root else (255,255,255)
                pygame.draw.circle(screen, col, (int(x),int(y)), 8)
                txt = font.render(n, True, col)
                screen.blit(txt, (x-10, y-25))

            # draw all saved lines so they stay connected
            for start, end in all_lines:
                pygame.draw.line(screen, (0,128,255), start, end, 3)

            pygame.display.flip()
            time.sleep(0.7)

            if root in positions:
                prev_pos = positions[root]

    running = False
